#!/usr/bin/env python3
"""file_organizer.py — Dọn dẹp & phân loại thư mục tự động (chạy 100% local).

Tính năng:
  1. Phân loại file theo extension vào các thư mục con (images/, documents/, ...).
  2. Đổi tên hàng loạt theo mẫu: <tien_to>-<so_thu_tu>.<ext> (có chế độ chạy thử --dry-run).
  3. Phát hiện file TRÙNG LẶP theo MD5.
  4. In báo cáo tổng hợp ra file organize_report.txt.

Không cần API, không cần cài thêm thư viện — chỉ dùng thư viện chuẩn Python.
"""
import argparse
import hashlib
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Nhóm extension -> thư mục đích khi phân loại
KINDS = {
    "images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "code": {".py", ".js", ".ts", ".c", ".cpp", ".java", ".sh", ".html", ".css"},
    "media": {".mp3", ".mp4", ".mkv", ".avi", ".wav", ".mov"},
}


def kind_of(path: Path) -> str:
    for kind, exts in KINDS.items():
        if path.suffix.lower() in exts:
            return kind
    return "others"


def md5_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def organize(folder: Path, report: list, dry: bool) -> None:
    """Bước 1: phân loại file vào thư mục con theo loại."""
    moved = defaultdict(int)
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        dest_dir = folder / kind_of(item)
        moved[kind_of(item)] += 1
        if not dry:
            dest_dir.mkdir(exist_ok=True)
            # Không ghi đè: thêm hậu số nếu trùng tên
            dest = dest_dir / item.name
            n = 1
            while dest.exists():
                dest = dest_dir / f"{item.stem}_{n}{item.suffix}"
                n += 1
            shutil.move(str(item), str(dest))
    for kind, count in sorted(moved.items()):
        report.append(f"Phan loai: {kind}/ <- {count} file")


def rename_batch(folder: Path, prefix: str, report: list, dry: bool) -> None:
    """Bước 2: doi ten hang loat file trong folder theo mau <prefix>-<i>.<ext>."""
    files = [p for p in sorted(folder.rglob("*")) if p.is_file() and not p.name.startswith(".")]
    for i, path in enumerate(files, 1):
        new_name = f"{prefix}-{i:03d}{path.suffix.lower()}"
        if path.name == new_name:
            continue
        report.append(f"Doi ten: {path.name} -> {new_name}")
        if not dry:
            path.rename(path.with_name(new_name))


def find_duplicates(folder: Path, report: list) -> None:
    """Bước 3: tim file trung lap theo MD5 (chi bao cao, khong tu xoa)."""
    by_hash = defaultdict(list)
    for path in folder.rglob("*"):
        if path.is_file() and not path.name.startswith("."):
            by_hash[md5_of(path)].append(path)
    groups = [paths for paths in by_hash.values() if len(paths) > 1]
    if not groups:
        report.append("Khong phat hien file trung lap.")
    for g in groups:
        report.append("Trung lap (" + g[0].name + "): " + ", ".join(str(p) for p in g))


def main() -> None:
    parser = argparse.ArgumentParser(description="Don dep & phan loai thu muc tu dong")
    parser.add_argument("folder", nargs="?", default=".", help="Thu muc can don (mac dinh: hien tai)")
    parser.add_argument("--dry-run", action="store_true", help="Chi in ke hoac, khong tao tac that")
    parser.add_argument("--rename-prefix", default="", help="Dat ten (vi du 'export') de doi ten hang lot")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        raise SystemExit(f"Khong phai thu muc: {folder}")

    report = [f"Bao cao don dep thu muc: {folder}",
              f"Thoi diem: {datetime.now():%Y-%m-%d %H:%M}",
              f"Che do: {'DRY-RUN' if args.dry_run else 'THUC THI'}", ""]
    find_duplicates(folder, report)
    if args.rename_prefix:
        rename_batch(folder, args.rename_prefix, report, args.dry_run)
    organize(folder, report, args.dry_run)

    report_path = folder / "organize_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\n>>> Da luu bao cao tai: {report_path}")


if __name__ == "__main__":
    main()
