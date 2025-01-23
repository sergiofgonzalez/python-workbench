"""App illustrating how dependencies are wired via Singleton Dependencies pattern."""

from datetime import datetime

import blog


def main() -> None:
    """Application entry point."""
    blog.init_db()
    posts = blog.get_all_posts()
    if len(posts) == 0:
        print(
            "No posts available. ",
            "Run `load_sample_posts.py` to create a few sample posts.",
        )

    for post in posts:
        print(post["title"])
        print("-" * len(post["title"]))
        print(
            f"Published on {datetime.strftime(post['created_at'], '%Y-%m-%d')}",
        )
        print(post["content"])
        print()


if __name__ == "__main__":
    main()
