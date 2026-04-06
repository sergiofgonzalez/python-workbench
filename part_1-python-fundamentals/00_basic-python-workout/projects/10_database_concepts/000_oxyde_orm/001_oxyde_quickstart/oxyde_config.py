"""Oxyde ORM configuration."""

# List of Python modules containing Model classes
MODELS = ["models"]

# Database dialect: "postgres", "sqlite", or "mysql"
DIALECT = "sqlite"

# Directory for migration files
MIGRATIONS_DIR = "migrations"

# Database connections
# Keys are connection aliases, values are connection URLs
DATABASES = {
    "default": "sqlite://./app.db",
}
