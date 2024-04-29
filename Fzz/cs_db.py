import csv
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn = sqlite3.connect('dbfiles/country.db')
cur = conn.cursor()

with open('data/match_base_data.csv') as f:
    reader = csv.reader(f)
    data = list(reader)


"""
#drop table
cur.execute('''DROP TABLE  matchbase''');
"""




# creating a table
cur.execute('''CREATE TABLE IF NOT EXISTS  matchbase (
CSCSITEID__C INTEGER ,
ACCOUNTNAMEENGLISH__C VARCHAR(250),
BRANCH_CUSTOMER_PARTY_KEY INTEGER ,
BRANCH_PRIMARY_NAME VARCHAR(250),
HQ_PRIMARY_NAME VARCHAR(250),
GU_PRIMARY_NAME VARCHAR(250),
BRANCH_ISO_COUNTRY_CD VARCHAR(250),
BRANCH_PARTY_SSOT_PARTY_ID_INT INTEGER ,
BRANCH_HQ_BRANCH_CD BOOLEAN,
EXACT_COUNTRY VARCHAR(250)
   )''')

for row in data:
    """
        cur.execute("INSERT INTO (CSCSITEID__C ,ACCOUNTNAMEENGLISH__C,BRANCH_CUSTOMER_PARTY_KEY,BRANCH_PRIMARY_NAME ,
        HQ_PRIMARY_NAME ,GU_PRIMARY_NAME ,BRANCH_ISO_COUNTRY_CD ,BRANCH_PARTY_SSOT_PARTY_ID_INT ,BRANCH_HQ_BRANCH_CD ,
        EXACT_COUNTRY ) values (?, ?,?, ?,?, ?,?, ?,?, ?)", row)
    """

    cur.execute("INSERT INTO  matchbase values(?, ?,?, ?,?, ?,?, ?,?, ?)", row)

# committing changes
conn.commit()
