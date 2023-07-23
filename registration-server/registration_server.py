from flask import Flask, request
import sqlite3
import backend_sql
import business_logic
import logging

# Setup Database
db_file:str  = "mock-kalay-network-registration-server.db"
sql_files:str = ["device_registration.sql", "device_credentials.sql"]

app:Flask = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
app.config


@app.route("/")
def index_endpoint()-> str:
    return "REGISTRATION SERVER! (CYSE 580 Final Project)"

@app.route("/register-device", methods=['POST'])
def register():
    json_data:dict[str, str] = request.get_json()
    connection:sqlite3.Connection = backend_sql.create_connection(db_file=db_file)
    
    if business_logic.register_device_with_database(connection, json_data=json_data):
        logging.info("SUCESSFULLY REGISTERED DEVICE")
        connection.close()
        return "SUCCESS"
    else:
        logging.error("FAILED TO REGISTER DEVICE")
        connection.close()
        return "FAILURE"

@app.route("/view-camera")
def view_camera():
    return ""
        

# Main function
if __name__ == "__main__":
    
    # Connect to database
    for sql_file in sql_files:
        connection:sqlite3.Connection = backend_sql.create_connection(db_file=db_file)
        if backend_sql.execute_sql(conn=connection, sql=backend_sql.load_database_table(sql_file=sql_file)) == False:
            exit(-1)
        connection.close()
        
    app.run(host="0.0.0.0", port="5000")