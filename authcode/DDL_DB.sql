CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    otp_secret VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_salt varchar(128)
);


CREATE TABLE roles (
    username varchar(255),
    role varchar(64),
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);


CREATE TABLE user_2fa_settings (
    user_id INT PRIMARY KEY,
    2fa_enabled BOOLEAN DEFAULT FALSE,
    method VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
