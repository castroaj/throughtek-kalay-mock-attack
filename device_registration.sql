CREATE TABLE IF NOT EXISTS device_registration (
    uuid VARCHAR(20) PRIMARY KEY NOT NULL,
    ip_address VARCHAR(15) NOT NULL,
    UNIQUE(uuid, ip_address)
);