import csv
import logging
# import sqlite3t
import warnings
warnings.filterwarnings('ignore')
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import pandas as pd

# Define the database connection parameters
db_params = {
    'host': 'db',
    'database': 'fuzzyappdatabase',
    'user': 'postgres',
    'password': 'test123',
    'port': 5880
}


print("connected to db")

# Connect to the 'soccer' database
db_params['database'] = 'fuzzyappdatabase'
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')

print("enigne is created")

conn = engine.connect(close_with_result=True)
result = conn.execute('SELECT count(*) as t FROM srilankainput;')
for row in result:
    if row['t'] == 0:
        result.close()

        print('engine is created')
        # Define the file paths for your CSV files
        csv_files = {
            'srilankainput': 'data/srilanka_base_data.csv',
            'matchbase': 'data/match_base_data.csv'
        }

        # Load and display the contents of each CSV file to check
        for table_name, file_path in csv_files.items():
            print(f"Contents of '{table_name}' CSV file:")
            df = pd.read_csv(file_path)
            print(df.head(2))  # Display the first few rows of the DataFrame
            print("\n")


        # Loop through the CSV files and import them into PostgreSQL
        for table_name, file_path in csv_files.items():
            df = pd.read_csv(file_path)
            df.to_sql(table_name, engine, if_exists='replace', index=False)

    else:
        print("There is data already in the table")

