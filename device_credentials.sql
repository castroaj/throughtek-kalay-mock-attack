CREATE TABLE IF NOT EXISTS device_credentials (
    uuid TEXT PRIMARY KEY,
    device_username TEXT NOT NULL,
    device_password TEXT NOT NULL,
    UNIQUE(uuid, device_username, device_password)
);