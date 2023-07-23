import http.client
import json
import argparse
import socket

def register_device(url:str,
                    port:int, 
                    uuid:str):
    
    endpoint:str = "/register-device"
    connection:http.client.HTTPConnection = http.client.HTTPConnection(host=url, port=port)

    hostname:str   =socket.gethostname()   
    ip_address:str =socket.gethostbyname(hostname)  

    data:dict[str, str] = { "uuid" : uuid, 
                            "ip_address" : ip_address }
    
    json_data = json.dumps(data)
    
    connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})

    response:http.client.HTTPResponse = connection.getresponse()
    print(response.read().decode())
    

def request_video(host:str,
                  port:int, 
                  uuid:str):
    yield
    
    
    
    
def main():
    parser:argparse.ArgumentParser = argparse.ArgumentParser()
    
    # Required
    parser.add_argument("-u", "--url", help="Target url", type=str, dest="url", default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Target port", type=int, dest="port", default="5000")
    parser.add_argument("-i", "--uuid", help="Device UUID", type=str, dest="uuid", default="12345678901234567890")
    
    # Actions
    parser.add_argument("-r", "--register", action="store_true")
    parser.add_argument("-v", "--request-video", type=bool, dest="video")
    
    args:argparse.Namespace = parser.parse_args()

    url:str = args.url
    port:int = args.port
    uuid:str = args.uuid
    
    register:bool = args.register
    video:bool    = args.video
    
    if register:
        register_device(url=url,
                        port=port,
                        uuid=uuid)
        
    if video:
        request_video(url=url,
                      port=port,
                      uuid=uuid)


if __name__ == "__main__":
    main()
