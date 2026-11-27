from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine import URL

from app.core.config import settings

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME,
)

engine = create_engine(
    DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True, pool_use_lifo=True
)


def get_session():
    with Session(engine) as session:
        yield session
