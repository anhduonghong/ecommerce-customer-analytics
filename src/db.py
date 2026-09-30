import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from . import config  # noqa: F401  (đảm bảo .env đã được load)


def get_engine():
    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url, pool_pre_ping=True)
