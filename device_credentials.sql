CREATE TABLE IF NOT EXISTS device_credentials (
    uuid VARCHAR(20) PRIMARY KEY,
    device_username VARCHAR(20) NOT NULL,
    device_password VARCHAR(20) NOT NULL,
    UNIQUE(uuid, device_username, device_password)
);