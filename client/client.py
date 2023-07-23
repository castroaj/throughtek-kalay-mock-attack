import http.client
import json
import argparse
import fcntl
import socket
import struct
import logging

def get_ip_address(interface) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packed_iface = struct.pack('256s', interface.encode('utf_8'))
    packed_addr = fcntl.ioctl(sock.fileno(), 0x8915, packed_iface)[20:24]
    return socket.inet_ntoa(packed_addr)

def register_device(reg_url:str,
                    reg_port:int, 
                    cam_url:str,
                    cam_port:int,
                    uuid:str,
                    nic:str) -> bool:
    
    endpoint:str = "/register-device"
    connection:http.client.HTTPConnection = http.client.HTTPConnection(host=reg_url, port=reg_port)

    ip_address = get_ip_address(nic)
    data:dict[str, str] = { 
                            "uuid" : uuid, 
                            "ip_address" : ip_address,
                            "cam_url"  : cam_url,
                            "cam_port" : cam_port
                          }
    
    json_data = json.dumps(data)
    connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})

    response:http.client.HTTPResponse = connection.getresponse()
    response_string:str = response.read().decode()
    
    if response_string == "SUCCESS": return True
    else:                            return False
    

def request_video(reg_url:str,
                  port:int, 
                  uuid:str):
    yield
    
    
    
    
def main():
    logging.basicConfig(level=logging.INFO)
    parser:argparse.ArgumentParser = argparse.ArgumentParser()
    
    # Required
    parser.add_argument("-u1", "--reg-url", help="Target registration server url", type=str, dest="reg_url", default="127.0.0.1")
    parser.add_argument("-p1", "--reg-port", help="Target registration server port", type=int, dest="reg_port", default="5000")
    parser.add_argument("-u2", "--cam-url", help="Target camera server url", type=str, dest="cam_url", default="127.0.0.1")
    parser.add_argument("-p2", "--cam-port", help="Target camera server port", type=int, dest="cam_port", default="5001")
    parser.add_argument("-i", "--uuid", help="Device UUID", type=str, dest="uuid", default="12345678901234567890")
    parser.add_argument("-n", "--nic", help="Communciation Network Interface", type=str, dest="nic", default="ens33")
    
    # Actions
    parser.add_argument("-r", "--register", action="store_true")
    parser.add_argument("-v", "--request-video", type=bool, dest="video")
    
    args:argparse.Namespace = parser.parse_args()

    reg_url:str  = args.reg_url
    reg_port:int = args.reg_port
    cam_url:str  = args.cam_url
    cam_port:str = args.cam_port
    uuid:str = args.uuid
    nic:str  = args.nic
    
    register:bool = args.register
    video:bool    = args.video
    
    logging.info("RESISTGRATION-SERVER-URL: %s, REGISTRATION-SEVER-PORT: %s, UUID: %s, NIC: %s, REGISTER-DEVICE: %s, REQUEST-VIDEO: %s" % (reg_url, reg_port, uuid, nic, register, video))
    
    if register and video:
        logging.error("You cannot register a device and request video in a single transaction")
    
    if register:
        logging.info("REGISTERING DEVICE (%s)" % uuid)
        if register_device(reg_url=reg_url,
                           reg_port=reg_port,
                           cam_url=cam_url,
                           cam_port=cam_port,
                           uuid=uuid,
                           nic=nic):
            logging.info("DEVICE SUCCESSFULLY REGISTERED (%s)" % uuid)
        else:
            logging.error("FAILED TO REGISTER DEVICE (%s)" % uuid)
        
    if video:
        logging.info("REQUESTING VIDEO FOOTAGE")
        request_video(url=reg_url,
                      port=reg_url,
                      uuid=uuid)


if __name__ == "__main__":
    main()
