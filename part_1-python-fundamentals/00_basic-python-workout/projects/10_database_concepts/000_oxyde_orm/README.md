# Oxyde ORM
> a type-safe, Pydantic-centric async ORM with a high-performance Rust core.

## Quick start

First, create a simple project and add `oxyde` as a dependency:

```bash
$ uv add oxyde
$ uv run oxyde init
🔧 Initializing Oxyde configuration...

📦 Models configuration
   Enter Python modules containing your Model classes.
   Examples: 'models', 'app.models', 'myapp.db.models'

   Models module(s) [models]:

🗄️  Database dialect
   Dialect (postgres/sqlite/mysql) [postgres]: sqlite

🔗 Database connection
   Database URL [postgresql://localhost/mydb]: sqlite://./app.db

📁 Migrations directory [migrations]:

✅ Configuration saved to oxyde_config.py

Next steps:
  1. Edit oxyde_config.py to adjust settings if needed
  2. Create your models in the specified module
  3. Run 'oxyde makemigrations' to generate migrations
  4. Run 'oxyde migrate' to apply migrations
```

Note that you need to use a relative path to refer to your SQLite db file `sqlite://./app.db`.

Note also the next steps. Because oxyde relies on certain code generation, you will need to run some commands once you have declared your models.

| NOTE: |
| :---- |
| `oxyde_config.py` can be manually updated without problems if you need to change details such as a the DB engine. |

Then, as a second step you will need to define the models in `models.py` (as configured when running `oxyde config`).

Right after that, you will need to generate the migration from your models.

```bash
$ uv run oxyde makemigrations
📝 Creating migrations...

0️⃣  Loading models...
   ✅ Imported 1 module(s)

1️⃣  Extracting schema from models...
   ✅ Found 1 table(s): users

2️⃣  Replaying existing migrations...
   📁 Creating migrations directory: /home/ubuntu/Development/git-repos/side-projects/python-workbench/part_1-python-fundamentals/00_basic-python-workout/projects/10_database_concepts/001_oxyde_orm/001_oxyde_quickstart/migrations
   ✅ Replayed 0 migration(s)

3️⃣  Computing diff...
   ✅ Found 1 operation(s):
      - Create table: users

4️⃣  Generating migration file...

   ✅ Created: migrations/0001_create_users_table.py

5️⃣  Generating type stubs...
Generated stub: /home/ubuntu/Development/git-repos/side-projects/python-workbench/part_1-python-fundamentals/00_basic-python-workout/projects/10_database_concepts/001_oxyde_orm/001_oxyde_quickstart/models.pyi
   ✅ Generated 1 stub file(s)
```


This will create all the necessary logic to create the tables representing the models if they don't exist already and populate them with the initial data, etc., but nothing will be applied.

In this step, the `models.pyi` file will also be created. This stub will contain all the necessary extra code to make your models type safe.

The next step will be to run the migration. This will create the tables by running the logic found in the migration files.

```bash
$ uv run oxyde migrate
⏳ Applying migrations...

Found 1 pending migration(s):
  - 0001_create_users_table

Migrating to latest...

✅ Applied 1 migration(s)
   - 0001_create_users_table
```

After this, you will find a generated `models.pyi` with information about the models.

Then, you'll be ready to write your application in `main.py`.

You have a runnable example in [Oxyde Quickstart](001_oxyde_quickstart/README.md)


Note the following:

When writing the models, you will need to use the following syntax:

```python
class User(Model):
    id: int | None = Field(default=None, db_pk=True)
    ...
```

Instead of:
```python
class User(Model):
    id: Annotated[int | None, Field(db_pk=True)]
    ...
```