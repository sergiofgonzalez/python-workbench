"""SQLite database initialization"""

import os
from pathlib import Path
from sqlite3 import Connection, Cursor, connect

from cryptid.utils.log_config import get_logger

conn: Connection | None = None
curs: Cursor | None = None

log = get_logger(__name__)

def get_db(name: str | None = None, reset: bool = False):
    """Connects to SQLite database file"""

    log.info("Initiating SQLite initialization: name=%s, reset=%s", name, reset)

    global conn, curs  # global will let us modify the value of those vars
    if conn:
        log.warning("conn was already set: returning")
        if not reset:
            return
        conn = None
    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB")
        prj_root_dir = Path(__file__).resolve().parents[1]
        db_dir = prj_root_dir / "db"
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()
    log.info("Successfuly initialized SQLite: name=%s", name)


get_db()
