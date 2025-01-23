"""Script that loads some sample posts in the blog db."""

from datetime import UTC, datetime

import blog

posts = [
    {
        "post_id": "my-first-post",
        "title": "My first post",
        "content": "Hello World!\nThis is my first post",
        "created_at": datetime.strptime("2024-02-03", "%Y-%m-%d")
        .astimezone(UTC)
        .date(),
    },
    {
        "post_id": "iterator-patterns",
        "title": "Python iterator patterns",
        "content": "Let's talk about some iterator patterns in Python\n\n...",
        "created_at": datetime.strptime("2023-02-06", "%Y-%m-%d")
        .astimezone(UTC)
        .date(),
    },
    {
        "post_id": "dependency-injection",
        "title": "Dependency injection in Node.js",
        "content": "Today we will discuss about dependency injection in Python\n\n...",
        "created_at": datetime.strptime("2020-02-29", "%Y-%m-%d")
        .astimezone(UTC)
        .date(),
    },
]

if __name__ == "__main__":
    blog.factory_reset_db()
    blog.init_db()
    for post in posts:
        blog.create_post(**post)
    print("All blog posts successfully imported!")
