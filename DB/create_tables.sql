CREATE TABLE IF NOT EXISTS notice_board (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    category VARCHAR(100),
    site VARCHAR(100),
    date DATETIME
);