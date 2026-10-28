# File Organizer

Sản phẩm tự động sinh bởi **Auto Python Factory** — 28/10/2026.

## Ý tưởng gốc (từ idea.txt)

```
Ý TƯỞNG (tự động chọn từ 10 từ khóa hot):
Chủ đề nóng nhất gần đây: dev, gemma, agent, built, first, local, model, why, actually, don
Bài viết tiêu biểu truyền cảm hứng: "SlothSRE (NapOps): An Overnight Gemma 4 & ADK Agent That Compresses 418 Lines of 3 AM Alerts into a 2-Line Morning Digest"

SẢN PHẨM ĐỀ XUẤT: Một script Python tên 'file_organizer.py' — công cụ
tự động hóa tệp tin theo từ khóa hot: quét một thư mục, tự phân loại
file theo extension và ngày tháng, đổi tên hàng loạt theo quy tắc, phát
hiện file trùng lặp (theo hash MD5) và in báo cáo dọn dẹp ra file text.
Chạy hoàn toàn local, không cần API, cài bằng 'pip install -r requirements.txt'(chỉ dùng thư viện chuẩn).
```

## Yêu cầu

- Python 3.10+ (chỉ dùng thư viện chuẩn — KHÔNG cần cài thêm gì).

## Cách sử dụng

```bash
# Xem kế hoạch mà không thay đổi gì (KHUYẾN KHÍCH chạy trước):
python file_organizer.py --dry-run /duong/dan/thu-muc

# Dọn dẹp thật:
python file_organizer.py /duong/dan/thu-muc

# Đổi tên hàng loạt kèm dọn dẹp:
python file_organizer.py --rename-prefix export /duong/dan/thu-muc
```

## Kết quả

- File được phân loại vào thư mục con: `images/`, `documents/`, `archives/`...
- Báo cáo ghi tại `organize_report.txt` trong thư mục đích.
- File trùng lặp (cùng MD5) được liệt kê — script KHÔNG tự xóa, bạn quyết định.

## giấy phép

MIT — tự do sử dụng, sửa đổi, phân phối.
