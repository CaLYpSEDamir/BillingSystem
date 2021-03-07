import databases
import sqlalchemy
from app.settings import db_config

DATABASE_URL = f"postgresql://" \
               f"{db_config.postgres_user}:{db_config.postgres_password}@" \
               f"{db_config.postgres_host}:{db_config.postgres_port}/" \
               f"{db_config.postgres_db}"

engine = sqlalchemy.create_engine(DATABASE_URL)
db = databases.Database(
    DATABASE_URL,
    min_size=db_config.pool_min_size,
    max_size=db_config.pool_max_size,
)

metadata = sqlalchemy.MetaData()


def create_tables():
    """Creating tables in db."""
    print('Staring tables creation.')
    metadata.create_all(engine)
    print('Tables are created.')
