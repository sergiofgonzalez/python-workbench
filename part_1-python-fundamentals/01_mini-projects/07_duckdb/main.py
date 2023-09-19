import duckdb
import pandas as pd

connection = duckdb.connect()

# Show the results
duckdb.sql("SELECT 42").show()

# Fetch the results
results = duckdb.sql("SELECT 42").fetchall()
print(results)

# Get a Pandas dataframe
results_df = duckdb.sql("SELECT 42").df()
print(results_df)


# Load and query CSV
duckdb.read_csv("data/tasks.csv")
duckdb.sql("""
           SELECT urgency, COUNT(*)
             FROM 'data/tasks.csv'
            WHERE status = '0'
         GROUP BY urgency
           """).show()

# Load and query JSON
duckdb.read_json("data/package.json")
duckdb.sql("SELECT * FROM 'data/package.json'").show()

dev_deps = duckdb.sql("SELECT devDependencies FROM 'data/package.json'").df()
print(dev_deps)

# Load and query Excel
df = pd.read_excel("data/rest-api-tools.xlsx")
duckdb.sql("SELECT * FROM df").show()