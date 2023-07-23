from io import TextIOWrapper
import sqlite3
from sqlite3 import Error
from typing import List

def create_connection(db_file):
    conn = None
    try:
        conn:sqlite3.Connection = sqlite3.connect(db_file)
        return conn
    except:
        return None
    
def execute_sql(conn, sql) -> bool:
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)
        return False
    conn.commit()
    return True

def load_database_table(sql_file:str) -> List[str]:
    sql_file:TextIOWrapper = open(sql_file)
    data:str = sql_file.read()
    sql_file.close
    return data

