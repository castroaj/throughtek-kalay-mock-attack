import backend_sql
import random
import string
import logging

def register_device_with_database(conn, json_data):
        
    def register_new_device(uuid:str, 
                            ip_address:str) -> bool:
        sql:str = """
            INSERT OR REPLACE INTO device_registration(uuid, ip_address) VALUES ("%s", "%s");
            """ % (uuid, ip_address)
        return backend_sql.execute_sql(conn, sql=sql)
    
    def register_device_credentials(uuid):
        
        device_username:str = "admin"
        device_password:str = ''.join(random.choices(string.ascii_uppercase +
                                                     string.digits, k=20))
        sql:str = """
                INSERT OR IGNORE INTO device_credentials(uuid, device_username, device_password) VALUES("%s", "%s", "%s");
                """ % (uuid, device_username, device_password)
        return backend_sql.execute_sql(conn, sql=sql) 
    
    uuid_tup:tuple = json_data["uuid"]
    uuid:str       = uuid_tup
    ip_address:str = json_data["ip_address"]

    if register_new_device(uuid=uuid, ip_address=ip_address) == False:
        logging.error("Failed to register device")
        return False

    if register_device_credentials(uuid=uuid) == False:
        logging.error("Failed to register device credentials")
        return False

    return True

