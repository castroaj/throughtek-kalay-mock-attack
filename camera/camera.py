from typing import Literal
from flask import Flask, request

app:Flask = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

# Setup Database
db_file:str  = "camera.db"

shared_secret_with_rs:str = "HO2ZVME32GG00X1YC7BO0XG3Y7EC97GDRIDEALI3VXU04T80PN9SQ72D4294"

@app.route("/")
def index_endpoint()-> str:
    return "CAMERA SERVER! (CYSE 580 Final Project)"

@app.route("/register-credentials", methods=['POST'])
def register_credentials() -> Literal['SUCCESS', 'FAILURE']:
    json_data:dict[str, str] = request.get_json()
    shared_secret:str = json_data['shared_secret_with_camera']
    print(json_data)
    if shared_secret == shared_secret_with_rs:
        return "SUCCESS"
    else:
        return "FAILURE"
    # if business_logic.register_device_with_database(connection, json_data=json_data):
    #     logging.info("SUCESSFULLY REGISTERED DEVICE")
    #     connection.close()
    #     return "SUCCESS"
    # else:
    #     logging.error("FAILED TO REGISTER DEVICE")
    #     connection.close()
    #     return "FAILURE"



@app.route("/footage", methods=['GET'])
def footage() -> str:
    args = request.args
    args.get("uuid")
    args.get("device_username")
    args.get("device_password")


# Main function
if __name__ == "__main__":    
    app.run(host="0.0.0.0", port="5001")