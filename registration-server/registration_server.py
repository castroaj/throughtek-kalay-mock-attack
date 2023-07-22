from flask import Flask, request
import sqlite3
import backend_sql

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
    backend_sql.register_device_with_database(connection, json_data=json_data)
    connection.close()
    return ""

@app.route("/view-camera")
def view_camera():
    return ""
        

# Main function
if __name__ == "__main__":
    
    # Connect to database
    for sql_file in sql_files:
        connection:sqlite3.Connection = backend_sql.create_connection(db_file=db_file)
        if backend_sql.create_table(conn=connection, create_table_sql=backend_sql.load_database_table(sql_file=sql_file)) == False:
            exit(-1)
        connection.close()
        
    app.run(host="0.0.0.0", port="5000")