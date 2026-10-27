-- Run once on a fresh machine.
-- WARNING: drops existing eventra_db.

DROP DATABASE IF EXISTS eventra_db;
CREATE DATABASE eventra_db;
USE eventra_db;

CREATE TABLE users (
    user_id   INT PRIMARY KEY AUTO_INCREMENT,
    name      VARCHAR(100) NOT NULL,
    email     VARCHAR(150) UNIQUE NOT NULL,
    phone     VARCHAR(15)  NOT NULL,
    password  VARCHAR(100) NOT NULL,
    role      ENUM('user','admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    event_id        INT PRIMARY KEY AUTO_INCREMENT,
    event_name      VARCHAR(200) NOT NULL,
    category        VARCHAR(50)  NOT NULL,
    description     TEXT,
    venue           VARCHAR(200) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    event_date      DATE NOT NULL,
    start_time      TIME NOT NULL,
    total_seats     INT NOT NULL,
    available_seats INT NOT NULL,
    ticket_price    DECIMAL(10,2) NOT NULL,
    organizer_id    INT,
    status          ENUM('Active','Cancelled','Completed') DEFAULT 'Active',
    FOREIGN KEY (organizer_id) REFERENCES users(user_id)
);

CREATE TABLE bookings (
    booking_id     INT PRIMARY KEY AUTO_INCREMENT,
    user_id        INT NOT NULL,
    event_id       INT NOT NULL,
    num_tickets    INT NOT NULL,
    total_amount   DECIMAL(10,2) NOT NULL,
    booking_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    booking_status ENUM('Confirmed','Cancelled') DEFAULT 'Confirmed',
    FOREIGN KEY (user_id)  REFERENCES users(user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

CREATE TABLE payments (
    payment_id     INT PRIMARY KEY AUTO_INCREMENT,
    booking_id     INT NOT NULL,
    amount         DECIMAL(10,2) NOT NULL,
    payment_mode   VARCHAR(20) NOT NULL,
    payment_status ENUM('Success','Failed','Refunded') DEFAULT 'Success',
    transaction_id VARCHAR(50) NOT NULL,
    payment_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);