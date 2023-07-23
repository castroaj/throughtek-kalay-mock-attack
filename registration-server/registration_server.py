from typing import Literal
from flask import Flask, request
import sqlite3
import backend_sql as backend_sql
import rs_business_logic
import logging

# Setup Database
db_file:str  = "rs-database.db"
sql_files:str = [ "rs_device_credentials.sql"]

# Shared secret
shared_secret_with_camera:str = "HO2ZVME32GG00X1YC7BO0XG3Y7EC97GDRIDEALI3VXU04T80PN9SQ72D4294"

app:Flask = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = False

@app.route("/")
def index_endpoint()-> str:
    return "REGISTRATION SERVER! (CYSE 580 Final Project)"

@app.route("/register-device", methods=['POST'])
def register() -> Literal['SUCCESS', 'FAILURE']:
    
    json_data:dict[str, str] = request.get_json()
    uuid:str = json_data['uuid']
    connection:sqlite3.Connection = backend_sql.create_connection(db_file=db_file)
    
    if rs_business_logic.register_device_with_database(connection, json_data=json_data, shared_secret_with_camera=shared_secret_with_camera):
        logging.info("SUCESSFULLY REGISTERED DEVICE (%s)" % uuid)
        connection.close()
        return "SUCCESS"
    else:
        logging.error("FAILED TO REGISTER DEVICE")
        connection.close()
        return "FAILURE"

@app.route("/client-request-credentials", methods=['POST'])
def view_camera():
    json_data:dict[str, str] = request.get_json()
    uuid:str = json_data['uuid']
    connection:sqlite3.Connection = backend_sql.create_connection(db_file=db_file)
    
    device_ip_adress, device_port, device_username, device_password = rs_business_logic.get_credentials_by_uuid(connection, uuid)
    
    if device_ip_adress is None or device_port is None or device_username is None or device_password is None:
        return "FAILURE"
    else:
        return device_ip_adress + ":" + str(device_port) + ":" + device_username + ":" + device_password
    
        

# Main function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Connect to database
    for sql_file in sql_files:
        connection:sqlite3.Connection = backend_sql.create_connection(db_file=db_file)
        if backend_sql.execute_sql(conn=connection, sql=backend_sql.load_database_table(sql_file=sql_file)) == False:
            exit(-1)
        connection.close()
    app.run(host="0.0.0.0", port="5000")