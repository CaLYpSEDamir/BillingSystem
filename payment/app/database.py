import databases
import sqlalchemy
from pydantic import BaseSettings

# from sqlalchemy.ext.declarative import declarative_base


class DBSettings(BaseSettings):
    postgres_host = 'localhost'
    postgres_port = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str


db_config = DBSettings()

DATABASE_URL = f"postgresql://" \
               f"{db_config.postgres_user}:{db_config.postgres_password}@" \
               f"{db_config.postgres_host}:{db_config.postgres_port}/" \
               f"{db_config.postgres_db}"

print(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
db = databases.Database(
    DATABASE_URL,
    min_size=5,
    max_size=10,
)
print("Init DB")
# Base = declarative_base()
metadata = sqlalchemy.MetaData()


def create_tables():
    """"""
    # Base.metadata.create_all(bind=engine)
    metadata.create_all(engine)
