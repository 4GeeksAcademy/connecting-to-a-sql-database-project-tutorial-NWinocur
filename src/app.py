import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, insert, select
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# 1) Connect to the database with SQLAlchemy
def connect():
    global engine
    try:
        connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT")
        engine.connect()
        print("Connected successfully!")
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

connect()

# 2) Create the tables

def execute_sql_file(filename: str):
    """
    Executes SQL commands from a .sql file using the global SQLAlchemy engine.
    Assumes that `connect()` has already defined the engine and connected to the DB.
    """
    try:
        # Ensure the engine is connected
        engine = connect()
        if engine is None:
            print("No database connection available.")
            return

        # Read SQL file
        with open(filename, 'r') as file:
            sql_script = file.read()

        # Split SQL script into individual statements
        # This simplistic splitter may need adjustment for more complex scripts
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

        with engine.connect() as connection:
            for statement in statements:
                print(f"Executing:\n{statement}")
                connection.execute(text(statement))

        print("SQL script executed successfully.")

    except Exception as e:
        print(f"Error executing SQL script: {e}")

execute_sql_file(".src/sql/create.sql")

# 3) Insert data

execute_sql_file(".src/sql/insert.sql")

# 4) Use Pandas to read and display a table

# Define SQL Query
sql_query = text("SELECT * FROM publishers")

# Load directly into DataFrame
with engine.connect() as conn:
    df = pd.read_sql(sql_query, conn)

print(df)


