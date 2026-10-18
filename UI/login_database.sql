CREATE DATABASE login;
use login;

CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50),
    username VARCHAR(100) NOT NULL,
    dob DATE,
    emailid VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
SELECT * FROM users;

SET SQL_SAFE_UPDATES = 0;
TRUNCATE TABLE users;
DELETE FROM users WHERE username = 'sanjukta2065';

UPDATE users SET username = CONCAT('@', username) WHERE username NOT LIKE '@%';
SET SQL_SAFE_UPDATES = 1;


