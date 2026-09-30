"""Cấu hình chung: đường dẫn + tham số pipeline."""
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

INCOMING_DIR = ROOT / "data" / "incoming"    # file CSV mới thả vào đây
ARCHIVE_DIR = ROOT / "data" / "archive"      # file đã nạp xong được chuyển sang đây
PROCESSED_DIR = ROOT / "data" / "processed"  # CSV output cho Power BI
IMAGES_DIR = ROOT / "images"
LOG_DIR = ROOT / "logs"

for d in (INCOMING_DIR, ARCHIVE_DIR, PROCESSED_DIR, IMAGES_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

TABLE_RETAIL = "retail"
# Notebook gốc gọi df.drop_duplicates() nhưng KHÔNG gán lại -> thực tế không loại trùng.
# Để False cho số liệu khớp dashboard hiện tại; đổi True nếu muốn loại trùng thật.
DROP_DUPLICATES = False
