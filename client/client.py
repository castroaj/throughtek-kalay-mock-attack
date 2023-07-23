import argparse
import logging
import yaml

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
                  cam_url:str,
                  cam_port:int):
    logging.info("REQUESTING VIDEO FOOTAGE")
    yield
    
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
    cam_url:str  = yaml_config["camera_url"]
    cam_port:str = yaml_config["camera_port"]
    uuid:str     = yaml_config["uuid"]
    
    logging.info("UUID: %s, RESISTGRATION-SERVER-URL: %s, REGISTRATION-SEVER-PORT: %s, CAMERA-URL: %s, CAMERA-PORT: %s" % (uuid, reg_url, reg_port, cam_url, cam_port))
    
    request_video(reg_url=reg_url,
                  reg_port=reg_port,
                  uuid=uuid,
                  cam_url=cam_url,
                  cam_port=cam_port)

if __name__ == "__main__":
    main()
