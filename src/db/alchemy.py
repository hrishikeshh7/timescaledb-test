import os
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker #sessionmaker to handle db


DBSession: sessionmaker = None
Base = None


class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = int(os.getenv("POSTGRES_PORT", 5432))  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
logger.debug("{settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL, connect_args={'connect_timeout': 2}, pool_size=0, max_overflow=-1,
                       pool_recycle=3600)

try:
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    logger.info("Database connected successfully")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as err:
    logger.error("Database Connection Error - {}".format(err))
