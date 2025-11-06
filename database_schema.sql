    -- Agricultural Data Management Database Schema
    -- Database: dbms_proj

    CREATE DATABASE IF NOT EXISTS dbms_proj;
    USE dbms_proj;

    -- Farmers table
    CREATE TABLE IF NOT EXISTS Farmers (
        farmer_id INT PRIMARY KEY AUTO_INCREMENT,
        farmer_name VARCHAR(255) NOT NULL,
        village VARCHAR(255),
        phone VARCHAR(20)
    );

    -- Crops table
    CREATE TABLE IF NOT EXISTS Crops (
        crop_id INT PRIMARY KEY AUTO_INCREMENT,
        crop_name VARCHAR(255) NOT NULL UNIQUE,
        season VARCHAR(50)
    );

    -- Markets table
    CREATE TABLE IF NOT EXISTS Markets (
        market_id INT PRIMARY KEY AUTO_INCREMENT,
        market_name VARCHAR(255) NOT NULL,
        location VARCHAR(255)
    );

    -- Transactions table
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INT PRIMARY KEY AUTO_INCREMENT,
        farmer_id INT,
        crop_id INT,
        market_id INT,
        quantity DECIMAL(10, 2) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (farmer_id) REFERENCES Farmers(farmer_id) ON DELETE CASCADE,
        FOREIGN KEY (crop_id) REFERENCES Crops(crop_id) ON DELETE CASCADE,
        FOREIGN KEY (market_id) REFERENCES Markets(market_id) ON DELETE CASCADE
    );

    -- Insert sample data
    INSERT INTO Farmers (farmer_id,farmer_name, village, phone) VALUES
    (1,'John Smith', 'Green Valley', '555-0101'),
    (2,'Maria Garcia', 'Sunrise Village', '555-0102'),
    (3,'Ahmed Hassan', 'Meadowbrook', '555-0103');

    INSERT INTO Crops (crop_name, season) VALUES
    ('Wheat', 'Winter'),
    ('Corn', 'Summer'),
    ('Rice', 'Monsoon'),
    ('Tomatoes', 'All Season');

    INSERT INTO Markets (market_name, location) VALUES
    ('Central Market', 'Downtown'),
    ('Farmers Market', 'City Square'),
    ('Wholesale Market', 'Industrial Area');

    INSERT INTO Transactions (farmer_id, crop_id, market_id, quantity, price) VALUES
    (1, 1, 1, 100.50, 2.50),
    (2, 2, 2, 75.25, 3.00),
    (3, 3, 3, 200.00, 1.75);
