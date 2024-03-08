# FastAPI: Database related considerations

## Relational databases

Python has a standard relational API definition called DB-API, and it's supported by Python driver packages for all major databases.

The following table lists the most common relational databases and their drivers:

| Database | OSS/Commercial | Python driver | URL |
| :------- | :------------- | :------------ | :-- |
| SQLite | OSS | sqlite3 | https://docs.python.org/3/library/sqlite3.html |
| PostgreSQL | OSS | psycopg2<br>asyncpg | https://github.com/psycopg/psycopg2<br>https://github.com/MagicStack/asyncpg |
| MySQL | OSS | MySQLdb<br>PyMySQL | https://mysqlclient.readthedocs.io/<br>https://pymysql.readthedocs.io/en/latest/ |
| SQL Server | Commercial | pyodbc<br>pymssql | https://mkleehammer.github.io/pyodbc/<br>https://pypi.org/project/pymssql/ |

Additional interesting packages related to SQL are:

+ [SQLAlchemy](https://www.sqlalchemy.org/) &mdash; a full-featured library, best known for its ORM capabilities.
+ [SQLModel](https://sqlmodel.tiangolo.com/) &mdash; a combination of SQLAlchemy and Pydantic, by the author of FastAPI.
+ [Records](https://github.com/kennethreitz/records) &mdash; a simple query API, from the author of the Requests.

### SQLAlchemy

#### Core

The base of SQLAlchemy is called Core and comprises:
+ An `Engine` object that implements the DB-API standard.
+ URLs that express the SQL server type and driver, and the specific database collection on that server.
+ Client-server connection pools.
+ Transactions (COMMIT and ROLLBACK support).
+ SQL dialect differences among various database types.
+ Direct SQL (text string) queries.
+ Queries in the SQLAlchemy Expression Language.

#### SQLAlchemy Expression Language

The SQLAlchemy Expression Language is a way of expressing queries against relational tables using Python classes such as `Table` and `Column`. It also defines `select()` and `insert()` for the operations.

These function will get translated to plain SQL string, but with the silver lining that it is independent of the specific server type.

#### ORM

An ORM expresses queries in terms of domain data models, instead of through relational tables and SQL logic.

### EdgeDB

[EdgeDB](https://www.edgedb.com/) is a new relational database written in Python. It uses PostgreSQL under the hood.

