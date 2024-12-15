
# Bank Management System

A desktop application developed in **Python** using **Tkinter** for the graphical user interface (GUI) and **MySQL** for backend database operations. This system provides essential banking functionalities such as account creation, secure fund transfers, loan applications, and transaction history management.

## Features

- **User Account Management**: Create and manage user accounts.
- **Secure Fund Transfers**: Transfer funds between accounts with ease and security.
- **Loan Applications**: Apply for loans, with admin approval or rejection.
- **Transaction History**: View detailed transaction records.
- **Admin Dashboard**:
  - Log in using predefined credentials (`username: admin`, `password: admin123`).
  - Manage user accounts, review transactions, and approve or reject loans.
- **Automated Updates**: Account balances are updated automatically upon loan approval.
- **Secure Access**: Password-protected user accounts and an admin login system to prevent unauthorized access.

## Technology Stack

- **Programming Language**: Python
- **GUI Library**: Tkinter
- **Database**: MySQL

## Requirements

Before running this application, ensure you have the following installed:

- Python 3.7 or higher
- MySQL Server
- Required Python libraries (can be installed via `requirements.txt`)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/bank-management-system.git
   cd bank-management-system
   ```

2. **Install Dependencies**:
   Install required Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Create a MySQL database named `bank_management`.
   - Import the provided `schema.sql` file to set up the database tables:
     ```bash
     mysql -u your_username -p bank_management < schema.sql
     ```

4. **Update Database Configuration**:
   Update the database connection details in the Python script:
   ```python
   host = "your_mysql_host"
   user = "your_mysql_username"
   password = "your_mysql_password"
   database = "bank_management"
   ```

5. **Run the Application**:
   Start the application by executing the main script:
   ```bash
   python app.py
   ```

## Usage

- **Users**: Log in with a valid username and password to perform banking operations.
- **Admin**: Log in with `username: Sagor` and `password: 1234` to access the admin dashboard.

## Screenshots

![Login Screen](screenshots/login_screen.png)
![Admin Dashboard](screenshots/admin_dashboard.png)

## Security Features

- Password-protected user accounts.
- Restricted admin access to sensitive data and operations.
- Secure database operations with MySQL.

## Contribution

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git commit -m "Add new feature"
   git push origin feature-name
   ```
4. Create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or issues, feel free to reach out to:
- Email: your-email@example.com
- GitHub: [your-username](https://github.com/your-username)
