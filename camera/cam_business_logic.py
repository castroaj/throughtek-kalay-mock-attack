import http.client
import json
import yaml


def load_yaml_config(args):
    file_stream = open(args.config_file)
    try:
        yaml_config = yaml.safe_load(file_stream)
    except yaml.YAMLError as e:
        print(e)
        exit(-1)
    return yaml_config

def register_device(reg_url:str,
                    reg_port:int, 
                    cam_url:str,
                    cam_port:int,
                    uuid:str) -> bool:
    
    endpoint:str = "/register-device"
    connection:http.client.HTTPConnection = http.client.HTTPConnection(host=reg_url, port=reg_port)

    data:dict[str, str] = { 
                            "uuid" : uuid, 
                            "cam_url"  : cam_url,
                            "cam_port" : cam_port
                          }
    
    json_data = json.dumps(data)
    connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})

    response:http.client.HTTPResponse = connection.getresponse()
    response_string:str = response.read().decode()
    
    if response_string == "SUCCESS": return True
    else:                            return False