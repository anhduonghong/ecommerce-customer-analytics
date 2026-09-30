"""Điểm vào duy nhất: python -m src.pipeline  [--force]
File này chỉ ĐIỀU PHỐI, logic nằm ở extract/transform/load/cohort/rfm/export."""
import argparse
import logging
import sys
from logging.handlers import RotatingFileHandler

from . import cohort, config, export, extract, load, rfm, transform
from .db import get_engine

log = logging.getLogger("pipeline")


def setup_logging():
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    fh = RotatingFileHandler(config.LOG_DIR / "pipeline.log", maxBytes=2_000_000, backupCount=5, encoding="utf-8")
    for h in (fh, logging.StreamHandler()):
        h.setFormatter(fmt)
        root.addHandler(h)


def run_etl() -> int:
    """Nạp mọi file CSV trong data/incoming. Trả về số file đã xử lý."""
    files = extract.list_incoming()
    if not files:
        log.info("Không có file mới trong %s", config.INCOMING_DIR)
        return 0
    engine = get_engine()
    for f in files:
        log.info("Xử lý %s", f.name)
        load.load(transform.transform(extract.read_csv(f)), engine)
        extract.archive(f)  # chỉ chuyển sau khi load thành công
    return len(files)


def run_analytics() -> None:
    engine = get_engine()
    df_cohort = cohort.compute(engine)
    rfm_df = rfm.compute(engine)
    seg = rfm.summarize(rfm_df)

    export.to_csv(df_cohort, rfm_df, seg)
    export.to_mysql(engine, df_cohort, rfm_df, seg)
    cohort.plot(df_cohort)
    rfm.plot(seg)
    log.info("Analytics xong: %s dòng cohort, %s khách RFM, %s segment",
             len(df_cohort), len(rfm_df), len(seg))


def main() -> int:
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="tính lại báo cáo dù không có file mới")
    args = parser.parse_args()
    try:
        n = run_etl()
        if n == 0 and not args.force:
            log.info("Bỏ qua bước analytics (dùng --force để chạy lại).")
            return 0
        run_analytics()
        log.info("Pipeline hoàn tất")
        return 0
    except Exception:
        log.exception("Pipeline THẤT BẠI")
        return 1


if __name__ == "__main__":
    sys.exit(main())
