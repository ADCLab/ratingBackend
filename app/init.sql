-- Create the database only if it doesn't exist
CREATE DATABASE IF NOT EXISTS ratingsDB;

-- Switch to the database
USE ratingsDB;

-- Create the Datasets table only if it doesn't exist
CREATE TABLE IF NOT EXISTS Datasets (
    d_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `description` VARCHAR(255) NOT NULL
);

-- Create the Commends table only if it doesn't exist
CREATE TABLE IF NOT EXISTS Comments (
    c_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    d_id INT UNSIGNED,
    FOREIGN KEY (d_id) REFERENCES Datasets(d_id) ON DELETE CASCADE
);

-- Create the Evaluators table only if it doesn't exist
CREATE TABLE IF NOT EXISTS Evaluators (
    u_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL
);

-- Create the Ratings table only if it doesn't exist
CREATE TABLE IF NOT EXISTS Ratings (
    d_id INT UNSIGNED,
    c_id INT UNSIGNED,
    u_id INT UNSIGNED,
    rating INT,
    flag BOOLEAN DEFAULT FALSE,
    skip BOOLEAN DEFAULT FALSE,
    other VARCHAR(255) DEFAULT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (d_id, c_id, u_id),
    FOREIGN KEY (d_id) REFERENCES Datasets(d_id) ON DELETE CASCADE,
    FOREIGN KEY (c_id) REFERENCES Commends(c_id) ON DELETE CASCADE,
    FOREIGN KEY (u_id) REFERENCES Evaluators(u_id) ON DELETE CASCADE
);

