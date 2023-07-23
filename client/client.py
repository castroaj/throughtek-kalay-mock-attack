import argparse
import logging
import yaml
import http.client
import json
import time


def load_yaml_config(args):
    file_stream = open(args.config_file)
    try:
        yaml_config = yaml.safe_load(file_stream)
    except yaml.YAMLError as e:
        print(e)
        exit(-1)
    return yaml_config

def request_video(reg_url:str,
                  reg_port:int, 
                  uuid:str,
                  duration=10):
    
    def get_cam_credentials():
        endpoint:str = "/client-request-credentials"
        connection:http.client.HTTPConnection = http.client.HTTPConnection(host=reg_url, port=reg_port)

        data:dict[str, str] = { 
                                "uuid" : uuid, 
                              }
        
        json_data = json.dumps(data)
        connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})

        response:http.client.HTTPResponse = connection.getresponse()
        response_string:str = response.read().decode()
        
        if response_string == "FAILURE":
            logging.error("INVALID CREDENTIALS")
            return (None, None)
        
        cam_info:list[str]     = response_string.split(":")
        print(cam_info)
        return (cam_info[0], cam_info[1], cam_info[2], cam_info[3])    

    def request_video_footage(device_ip_address,
                              device_port,
                              device_username,
                              device_password):
        endpoint:str = "/video-footage"
        connection:http.client.HTTPConnection = http.client.HTTPConnection(host=device_ip_address, port=device_port)

        data:dict[str, str] = { 
                                "uuid" : uuid, 
                                "device_username" : device_username, 
                                "device_password" : device_password
                              }
        
        json_data = json.dumps(data)
        try:
            connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})
        except:
            return "FAILED TO AQUIRE VIDEO FOOTAGE... ATTEMPT MADE TO '%s:%s'" % (cam_url, cam_port)

        response:http.client.HTTPResponse = connection.getresponse()
        response_string:str = response.read().decode()
        return response_string

    logging.info("REQUESTING CAMERA CREDS FROM REGISTRATION SERVER...")
    time.sleep(1)
    device_ip_address, device_port, device_username, device_password = get_cam_credentials()

    if device_username is None or device_password is None:
        logging.error("FAILED TO GET CREDENTIALS (%s)" % uuid)
        return False
    
    logging.info("AQUIRED CREDS FROM REGISTRATION SERVER (%s:%s)" % (device_username, device_password))
    time.sleep(2.5)
    
    for _ in range(duration):
        video_data = request_video_footage(device_ip_address=device_ip_address,
                                                device_port=device_port,
                                                device_username=device_username,
                                                device_password=device_password)
        print(video_data)
        time.sleep(0.5)
    
    
    
def main():
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file",  help="Target domain for scraping", type=str, dest="config_file", default="client_config.yml")
    
    args = parser.parse_args()

    if args.config_file is None or args.config_file == "":
        print("Configuration file must be provided")
        print("EXITING")
        exit(-1)
        
    yaml_config = load_yaml_config(args)

    reg_url:str  = yaml_config["registration_server_url"]
    reg_port:int = yaml_config["registration_server_port"]
    uuid:str     = yaml_config["uuid"]
    duration:int = yaml_config["duration"]
    
    logging.info("UUID: %s, RESISTGRATION-SERVER-URL: %s, REGISTRATION-SEVER-PORT: %s, DURATION: %s" % (uuid, reg_url, reg_port, duration))
    request_video(reg_url=reg_url,
                  reg_port=reg_port,
                  uuid=uuid,
                  duration=duration)

if __name__ == "__main__":
    main()
