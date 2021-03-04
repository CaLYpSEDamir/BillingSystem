from databases import Database
from app.database import db


def get_db() -> Database:
    """Returning global `db` entity."""
    return db
