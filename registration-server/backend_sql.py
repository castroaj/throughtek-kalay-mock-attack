from io import TextIOWrapper
import sqlite3
from sqlite3 import Error
from typing import List


def register_device_with_database(conn, json_data):
    
    uuid:str       = json_data["uuid"], 
    ip_address:str = json_data["ip_address"]
    if insert_update_registration_table(conn, uuid=uuid, ip_address=ip_address) == False:
        print("Failed to insert record")
        return False

    return True

def create_connection(db_file):
    conn = None
    try:
        conn:sqlite3.Connection = sqlite3.connect(db_file)
        return conn
    except:
        return None
    
def create_table(conn, create_table_sql) -> bool:
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        return False
    return True

def insert_update_registration_table(conn,
                                     uuid, 
                                     ip_address):
    sql:str = """
              INSERT OR REPLACE INTO device_registration(uuid, ip_address) VALUES('uuid', "%s"), ('ip_address', "%s");
              """ % (uuid, ip_address)
    
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

