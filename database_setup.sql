-- Create bank_system database
CREATE DATABASE bank_system;
USE bank_system;

-- Accounts Table
CREATE TABLE accounts (
    acc_num VARCHAR(20) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    acc_type ENUM('Savings', 'Current') NOT NULL,
    email VARCHAR(100) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    dob DATE NOT NULL
);

-- Transactions Table
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    acc_num VARCHAR(20) NOT NULL,
    transaction_date DATETIME NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    type ENUM('deposit', 'withdraw', 'transfer', 'loan') NOT NULL,
    FOREIGN KEY (acc_num) REFERENCES accounts(acc_num)
);

-- Loans Table
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    acc_num VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (acc_num) REFERENCES accounts(acc_num)
);