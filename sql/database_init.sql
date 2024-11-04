CREATE DATABASE leave_management_system;
USE leave_management_system;

CREATE TABLE leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50),
    employee_name VARCHAR(100),
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    reason TEXT
);
select * from leave_requests;
CREATE TABLE approved_leave (
    employee_id INT NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    leave_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('employee', 'manager')
);

select * from approved_leave;