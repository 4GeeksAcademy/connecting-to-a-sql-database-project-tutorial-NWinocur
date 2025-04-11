import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, insert, select
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# 1) Connect to the database with SQLAlchemy
# Connect to SQLite database
engine = create_engine('sqlite:///students.db', echo=False)


# 2) Create the tables

# Metadata object to hold schema
metadata = MetaData()

# Define the students table
students = Table(
    'students',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer),
    Column('grade', String)
)

# Create the table in the database
metadata.create_all(engine)


# 3) Insert data

with engine.connect() as conn:
    with conn.begin():  # <-- this will commit automatically
        conn.execute(
            students.insert(),
            [
                {"name": "John Doe", "age": 20, "grade": "A"},
                {"name": "Jane Smith", "age": 21, "grade": "B"},
                {"name": "Alice Johnson", "age": 22, "grade": "A"},
                {"name": "Bob Brown", "age": 19, "grade": "C"},
                {"name": "Charlie Davis", "age": 23, "grade": "B"},
            ]
        )

print("Database created and data inserted successfully!")


# 4) Use Pandas to read and display a table

# Define SQL Query
sql_query = text("SELECT * FROM students")

# Load directly into DataFrame
with engine.connect() as conn:
    df = pd.read_sql(sql_query, conn)

print(df)


