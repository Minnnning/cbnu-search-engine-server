CREATE TABLE IF NOT EXISTS notice_board (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    url VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    category VARCHAR(100),
    site VARCHAR(100),
    date DATETIME
);

CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,         
    restaurantId INT NOT NULL,                 
    restaurant_name VARCHAR(255) NOT NULL,  
    menu TEXT NOT NULL,                        
    time INT NOT NULL,                        
    date DATE NOT NULL                        
);