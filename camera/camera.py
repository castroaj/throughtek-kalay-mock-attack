from typing import Literal
from flask import Flask, request
import logging
import argparse
import cam_business_logic
from multiprocessing import Process
import time 
import os

app:Flask = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = False

shared_secret_with_rs:str = "HO2ZVME32GG00X1YC7BO0XG3Y7EC97GDRIDEALI3VXU04T80PN9SQ72D4294"

device_registered = False
device_uuid = None
device_username = None
device_password = None

@app.route("/")
def index_endpoint()-> str:
    return "CAMERA SERVER! (CYSE 580 Final Project)"

@app.route("/register-credentials", methods=['POST'])
def register_credentials() -> Literal['SUCCESS', 'FAILURE']:
    
    global device_registered
    global device_uuid
    global device_username
    global device_password
    
    json_data:dict[str, str] = request.get_json()
    shared_secret:str = json_data['shared_secret_with_camera']
    
    if shared_secret == shared_secret_with_rs:
        
        if device_registered == False:
            device_registered    = True
            device_uuid     = json_data['uuid']
            device_username = json_data['device_username']
            device_password = json_data['device_password']
            logging.info("DEVICE UUID/CREDENTIALS REGISTERED (%s)" % (device_uuid))
            logging.debug("uuid: %s, user: %s, pass: %s" % (device_uuid, device_username, device_password))
        else:
            logging.info("DEVICE ALREADY REGISTERED (%s)" % (device_uuid))
            logging.debug("uuid: %s, user: %s, pass: %s" % (device_uuid, device_username, device_password))
            
        return "SUCCESS"
    else:
        return "FAILURE"

@app.route("/video-footage", methods=['POST'])
def footage() -> str:
    json_data:dict[str, str] = request.get_json()
    json_uuid     = json_data['uuid']
    json_username = json_data['device_username']
    json_password = json_data['device_password']
    
    if device_uuid == json_uuid:
        if device_username == json_username and device_password == json_password:
            return str(bytearray(os.urandom(1000)))
        else:
            return "INCORRECT USER/PASSWORD. DENIED"
    else:
        return "INCORRECT UUID. DENIED"

def start_flask(camera_url,
                camera_port):
    app.run(host=camera_url, port=camera_port)
    

# Main function
if __name__ == "__main__":    
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file",  help="Target domain for scraping", type=str, dest="config_file", default="camera_config.yml")
    args = parser.parse_args()

    if args.config_file is None or args.config_file == "":
        print("Configuration file must be provided")
        print("EXITING")
        exit(-1)
        
    yaml_config = cam_business_logic.load_yaml_config(args)
    
    p = Process(target=start_flask, args=(yaml_config["camera_url"], yaml_config["camera_port"]))
    p.start()
    
    logging.info("STARTING CAMERA SERVER")
    time.sleep(1)
    logging.info("ATTEMPTING TO REGISTER DEVICE (%s)" % yaml_config["uuid"])
    
    cam_business_logic.register_device(reg_url=yaml_config["registration_server_url"],
                                       reg_port=yaml_config["registration_server_port"],
                                       cam_url=yaml_config["camera_url"],
                                       cam_port=yaml_config["camera_port"],
                                       uuid=yaml_config["uuid"])
    
    
