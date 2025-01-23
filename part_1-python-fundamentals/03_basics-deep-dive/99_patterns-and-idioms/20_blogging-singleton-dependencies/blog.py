"""blog.py: module with the API to create and retrieve blog posts, and init the db."""

from datetime import UTC, date, datetime

from db import db_conn


def init_db() -> None:
    """Initialize the blog database."""
    init_statement = """
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor = db_conn.cursor()
    cursor.execute(init_statement)
    db_conn.commit()


def factory_reset_db() -> None:
    """Drop the blog table from the database to start from scratch."""
    cursor = db_conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS posts")
    db_conn.commit()


def create_post(post_id: str, title: str, content: str, created_at: date) -> None:
    """Save a new blog post in the db."""
    query = """
        INSERT INTO posts
        VALUES (:id, :title, :content, :created_at)
    """
    post_dict = {
        "id": post_id,
        "title": title,
        "content": content,
        "created_at": created_at,
    }
    cursor = db_conn.cursor()
    cursor.execute(query, post_dict)
    db_conn.commit()


def _row_to_dict(row: tuple[str, str, str, date]) -> dict[str, str, str, date]:
    """Map a row from the database into the corresponding dictionary object."""
    post_id, title, content, created_at = row
    return {
        "post_id": post_id,
        "title": title,
        "content": content,
        "created_at": datetime.strptime(created_at, "%Y-%m-%d").astimezone(UTC).date(),
    }


def get_all_posts() -> dict[str, str, str, date]:
    """Return all blog posts from the db."""
    query = """
        SELECT * FROM posts
        ORDER BY created_at DESC
    """
    cursor = db_conn.cursor()
    cursor.execute(query)
    rows = list(cursor.fetchall())
    return [_row_to_dict(row) for row in rows]
