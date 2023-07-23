import backend_sql as backend_sql
import random
import string
import logging
import http
import json

def register_device_with_database(conn, 
                                  json_data,
                                  shared_secret_with_camera) -> bool:
        
    def register_new_device(uuid:str, 
                            ip_address:str) -> bool:
        sql:str = """
            INSERT OR REPLACE INTO device_registration(uuid, ip_address) VALUES ("%s", "%s");
            """ % (uuid, ip_address)
        return backend_sql.execute_sql(conn, sql=sql)
    
    def register_device_credentials(uuid,
                                    cam_url:str,
                                    cam_port:int) -> bool:
        
        def determine_device_credentials():
            
            sql_registration_test:str = """
                                        SELECT device_username, device_password FROM device_credentials where uuid = "%s"
                                        """ % (uuid)

            rows = backend_sql.execute_sql_query(conn, sql=sql_registration_test)
            
            if rows is not None and len(rows) == 1:
                device_username = rows[0][0]
                device_password = rows[0][1]
            else:
                device_username:str   = "admin"
                device_password:str   = ''.join(random.choices(string.ascii_uppercase +
                                                            string.digits, k=20))
            return (device_username, device_password)
        
        def register_device_on_camera(device_username:str,
                                      device_password:str) -> bool:
            endpoint:str = "/register-credentials"
            connection:http.client.HTTPConnection = http.client.HTTPConnection(host=cam_url, port=cam_port)

            data:dict[str, str] = { 
                                    "uuid" : uuid, 
                                    "device_username" : device_username,
                                    "device_password"  : device_password,
                                    "shared_secret_with_camera" : shared_secret_with_camera
                                  }
            
            json_data = json.dumps(data)
            try:
                connection.request('POST', endpoint, json_data, headers={"Content-Type" : "application/json"})
            except:
                logging.error("CAMERA IS NOT ACTIVE")
                return False

            response:http.client.HTTPResponse = connection.getresponse()
            response_string:str = response.read().decode()
            if response_string == "SUCCESS": return True
            else:                            return False
        
        device_username, device_password = determine_device_credentials()
  
        sql:str = """
                INSERT OR IGNORE INTO device_credentials(uuid, device_username, device_password, device_ip_address, device_port) VALUES("%s", "%s", "%s", "%s", %s);
                """ % (uuid, device_username, device_password, cam_url, cam_port)
        
        if register_device_on_camera(device_username=device_username, device_password=device_password) == False:
            return False
        logging.info("SUCCESSFULLY LOADED CREDENTIALS ON CAMERA USING SHARED SECRET")
        
        if backend_sql.execute_sql(conn, sql=sql) == False:
            return False
        logging.info("SUCCESSFULLY LOADED ")
        
        return True
    
    uuid_tup:tuple = json_data["uuid"]
    uuid:str       = uuid_tup
    ip_address:str = json_data["ip_address"]
    cam_url:str    = json_data["cam_url"]
    cam_port:int   = json_data["cam_port"]

    if register_new_device(uuid=uuid, 
                           ip_address=ip_address) == False:
        logging.error("Failed to register device")
        return False

    if register_device_credentials(uuid=uuid, 
                                   cam_url=cam_url, 
                                   cam_port=cam_port) == False:
        logging.error("Failed to register device credentials")
        return False
    return True
