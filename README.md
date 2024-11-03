# Employee-Leave-Management-System
A web-based Employee Leave Management System built with Flask and MySQL, allowing employees to submit leave requests and managers to review and approve them. The system features user authentication, leave request tracking, and a dashboard for both employees and managers.
# Employee Leave Management System

## Project Overview
The Employee Leave Management System is a web application designed to streamline the process of leave requests and approvals within an organization. It provides a user-friendly interface for employees to submit leave requests and for managers to review and approve them. The system is built using Flask for the backend and uses a MySQL database for data storage.

## Features

### User Roles
- **Employee**
  - Register for an account using email and password.
  - Submit leave requests, including leave type, start date, end date, and reason.
  - View leave balance and history of approved leaves.
  
- **Manager**
  - Approve or reject leave requests submitted by employees.
  - View all leave requests with the ability to filter and sort by employee or date.

### Functionalities
- **User Authentication**
  - User registration and login functionality.
  - Google login option for quick access.
  
- **Leave Request Management**
  - Employees can submit leave requests.
  - Leave requests are routed to managers for approval.
  
- **Leave Approval Workflow**
  - Managers can approve or reject leave requests.
  - Comments can be added for approved/rejected requests.
  
- **Leave Balance Tracking**
  - Displays total leave entitlement and the remaining balance for each employee.
  
- **Calendar View**
  - Visual representation of leave schedules and availability, highlighting approved leaves.
  
- **User Dashboard**
  - Separate dashboards for employees and managers.
  
- **Error Handling**
  - Custom error messages for common issues like invalid credentials or internal server errors.

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python with Flask
- **Database:** MySQL
- **Libraries:** `Flask`, `pymysql`

## Database Schema
### Users Table
| Column Name      | Data Type         |
|------------------|-------------------|
| employee_name    | VARCHAR            |
| email            | VARCHAR            |
| password         | VARCHAR            |
| role             | ENUM (employee, manager) |

### Leave Requests Table
| Column Name      | Data Type         |
|------------------|-------------------|
| employee_id      | INT (Foreign Key) |
| employee_name    | VARCHAR            |
| leave_type       | VARCHAR            |
| start_date       | DATE              |
| end_date         | DATE              |
| reason           | TEXT              |
| status           | ENUM (Pending, Approved, Rejected) |

### Approved Leaves Table
| Column Name      | Data Type         |
|------------------|-------------------|
| employee_id      | INT (Foreign Key) |
| employee_name    | VARCHAR            |
| leave_type       | VARCHAR            |
| start_date       | DATE              |
| end_date         | DATE              |
| reason           | TEXT              |

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sworaj2002/employee-leave-management-system.git
   cd employee-leave-management-system
