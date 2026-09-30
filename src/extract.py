"""EXTRACT: tìm file mới, đọc CSV, lưu trữ file sau khi xử lý."""
import logging
import shutil
from datetime import datetime

import pandas as pd

from . import config

log = logging.getLogger(__name__)


def list_incoming():
    return sorted(config.INCOMING_DIR.glob("*.csv"))


def read_csv(path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="ISO-8859-1")


def archive(path) -> None:
    dest = config.ARCHIVE_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{path.name}"
    shutil.move(str(path), dest)
    log.info("Đã chuyển %s -> archive", path.name)
