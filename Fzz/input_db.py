import csv
# import sqlite3
from sqlalchemy import create_engine
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




"""
# Create a cursor object
cur = conn.cursor()

# Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
conn.set_session(autocommit=True)

# Create the 'soccer' database
cur.execute("CREATE DATABASE soccer")

# Commit the changes and close the connection to the default database
conn.commit()
cur.close()
conn.close()


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test123@localhost:5880/fuzzyappdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


conn = psycopg2.connect(database="fuzzyappdatabase",
                        user="postgres",
                        host='localhost',
                        password="test123",
                        port=5880)

# conn = sqlite3.connect('fuzzyappdatabase.db')
cur = conn.cursor()


with open('data/srilanka_base_data.csv') as f:
    reader = csv.reader(f)
    data = list(reader)


#drop table
cur.execute('''DROP TABLE  srilankainput''');


csv_files = {
    'srilankainput': '/Users/rsherlek/Documents/fastapi/Fzz/data/srilanka_base_data.csv'

}



# creating a table
cur.execute('''CREATE TABLE IF NOT EXISTS  srilankainput (
ACCOUNT_NAME VARCHAR(250),
LEAD_ID VARCHAR(250),
GOMINE_ACCOUNT VARCHAR(250),
ACCOUNT_MATCH_TYPE VARCHAR(250),
PARTNER_COUNTRY VARCHAR(250), 
ORIGINAL_LV_000 INTEGER,
REPORTED_LV_000 INTEGER
   )''')


for table_name, file_path in csv_files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)






for row in data:
    
        cur.execute("INSERT INTO (CSCSITEID__C ,ACCOUNTNAMEENGLISH__C,BRANCH_CUSTOMER_PARTY_KEY,BRANCH_PRIMARY_NAME ,
        HQ_PRIMARY_NAME ,GU_PRIMARY_NAME ,BRANCH_ISO_COUNTRY_CD ,BRANCH_PARTY_SSOT_PARTY_ID_INT ,BRANCH_HQ_BRANCH_CD ,
        EXACT_COUNTRY ) values (?, ?,?, ?,?, ?,?, ?,?, ?)", row)
    

    cur.execute("INSERT INTO  srilankainput  values(?, ?,?, ?,?, ?,?)", row)

# committing changes
conn.commit()

"""