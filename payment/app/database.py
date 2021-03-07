import databases
import sqlalchemy
from pydantic import BaseSettings


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

engine = sqlalchemy.create_engine(DATABASE_URL)
db = databases.Database(
    DATABASE_URL,
    min_size=5,
    max_size=10,
)

metadata = sqlalchemy.MetaData()


def create_tables():
    """Creating tables in db."""
    print('Staring tables creation.')
    metadata.create_all(engine)
