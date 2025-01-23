"""blog.py: module with the API to create and retrieve blog posts, and init the db."""

from datetime import UTC, date, datetime
from sqlite3 import Connection


class Blog:
    """Blog class."""

    def __init__(self, db: Connection) -> None:
        """Initialize an instance of the Blog class."""
        self.db = db

    def init_db(self) -> None:
        """Initialize the blog database."""
        init_statement = """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor = self.db.cursor()
        cursor.execute(init_statement)
        self.db.commit()

    def factory_reset_db(self) -> None:
        """Drop the blog table from the database to start from scratch."""
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS posts")
        self.db.commit()

    def create_post(
        self,
        post_id: str,
        title: str,
        content: str,
        created_at: date,
    ) -> None:
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
        cursor = self.db.cursor()
        cursor.execute(query, post_dict)
        self.db.commit()

    def get_all_posts(self) -> dict[str, str, str, date]:
        """Return all blog posts from the db."""
        query = """
            SELECT * FROM posts
            ORDER BY created_at DESC
        """
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = list(cursor.fetchall())
        return [Blog._row_to_dict(row) for row in rows]

    @staticmethod
    def _row_to_dict(row: tuple[str, str, str, date]) -> dict[str, str, str, date]:
        """Map a row from the database into the corresponding dictionary object."""
        post_id, title, content, created_at = row
        return {
            "post_id": post_id,
            "title": title,
            "content": content,
            "created_at": datetime.strptime(created_at, "%Y-%m-%d")
            .astimezone(UTC)
            .date(),
        }
