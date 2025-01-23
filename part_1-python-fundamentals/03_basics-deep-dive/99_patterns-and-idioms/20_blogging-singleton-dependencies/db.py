"""db.py: The database module for the blogging system using SQLite."""

from pathlib import Path
from sqlite3 import connect

_prj_root_dir = Path(__file__).resolve().parents[0]
_db_path = _prj_root_dir / "blog_db" / "blog_db_data.sqlite"

db_conn = connect(_db_path)
