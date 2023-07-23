import backend_sql
import random
import string

def register_device_with_database(conn, json_data):
    
    def register_device(uuid:str, 
                        ip_address:str) -> bool:
        sql:str = """
            INSERT OR REPLACE INTO device_registration(uuid, ip_address) VALUES('uuid', "%s"), ('ip_address', "%s");
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
    
    uuid:str       = json_data["uuid"], 
    ip_address:str = json_data["ip_address"]

    if register_device(uuid=uuid, ip_address=ip_address) == False:
        print("Failed to register device")
        return False

    if register_device_credentials(uuid=uuid) == False:
        print("Failed to register device credentials")
        return False

    return True

