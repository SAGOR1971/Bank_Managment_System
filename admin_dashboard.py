import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection

def admin_dashboard(root):
    """
    Admin Dashboard for managing accounts, loans, and transactions.
    """
    def login_admin():
        """
        Handles admin login and validates the credentials.
        """
        username = admin_user.get()
        password = admin_pass.get()
        
        if username == "admin" and password == "admin123":
            admin_login.destroy()
            admin_panel()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def admin_panel():
        """
        Displays the admin dashboard with options to view accounts, loans, and transactions.
        """
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Dashboard")
        admin_window.geometry("500x600")

        def view_accounts():
            """
            Displays a window with a list of all user accounts.
            """
            db = DatabaseConnection()
            accounts = db.fetch_all("SELECT * FROM accounts")
            
            accounts_window = tk.Toplevel(admin_window)
            accounts_window.title("All Accounts")
            accounts_window.geometry("800x600")
            
            tree = ttk.Treeview(accounts_window, columns=('Account', 'Name', 'Type', 'Balance'), show='headings')
            tree.heading('Account', text='Account Number')
            tree.heading('Name', text='User Name')
            tree.heading('Type', text='Account Type')
            tree.heading('Balance', text='Balance')
            
            for account in accounts:
                tree.insert('', 'end', values=(
                    account['acc_num'], 
                    account['user_name'], 
                    account['acc_type'], 
                    account['balance']
                ))
            
            tree.pack(fill='both', expand=True)
            db.close_connection()

        def view_transactions():
            """
            Displays a window with a list of all transactions.
            """
            db = DatabaseConnection()
            transactions = db.fetch_all("SELECT * FROM transactions")
            
            transaction_window = tk.Toplevel(admin_window)
            transaction_window.title("Transactions")
            transaction_window.geometry("800x600")
            
            tree = ttk.Treeview(transaction_window, columns=('Account', 'Date', 'Amount', 'Type'), show='headings')
            tree.heading('Account', text='Account Number')
            tree.heading('Date', text='Transaction Date')
            tree.heading('Amount', text='Amount')
            tree.heading('Type', text='Transaction Type')
            
            for txn in transactions:
                tree.insert('', 'end', values=(
                    txn['acc_num'], 
                    txn['transaction_date'], 
                    txn['amount'], 
                    txn['type']
                ))
            
            tree.pack(fill='both', expand=True)
            db.close_connection()

        def manage_loans():
            """
            Displays a window with a list of all loans, and allows approving or rejecting pending loans.
            """
            db = DatabaseConnection()
            loans = db.fetch_all("SELECT l.*, a.user_name FROM loans l JOIN accounts a ON l.acc_num = a.acc_num")

            def approve_loan(loan_id, acc_num, amount):
                """
                Approves a loan, updates the account balance, and creates a loan transaction.
                """
                db = DatabaseConnection()
                db.execute_query("UPDATE loans SET status='Approved' WHERE id=%s", (loan_id,))
                db.execute_query("UPDATE accounts SET balance = balance + %s WHERE acc_num = %s", (amount, acc_num))
                db.execute_query(
                    "INSERT INTO transactions (acc_num, transaction_date, amount, type) VALUES (%s, NOW(), %s, 'loan')",
                    (acc_num, amount)
                )
                db.close_connection()
                messagebox.showinfo("Success", f"Loan Approved! {amount} added to account {acc_num}")
                loans_window.destroy()
                manage_loans()

            def reject_loan(loan_id):
                """
                Rejects a loan and updates the loan status.
                """
                db = DatabaseConnection()
                db.execute_query("UPDATE loans SET status='Rejected' WHERE id=%s", (loan_id,))
                db.close_connection()
                messagebox.showinfo("Success", "Loan Rejected!")
                loans_window.destroy()
                manage_loans()

            loans_window = tk.Toplevel(admin_window)
            loans_window.title("Manage Loans")
            loans_window.geometry("900x600")
            
            # Create a frame to hold the Treeview and allow scrolling
            frame = tk.Frame(loans_window)
            frame.pack(fill='both', expand=True)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')

            tree = ttk.Treeview(frame, columns=('Loan ID', 'Account', 'User Name', 'Amount', 'Status'), 
                                show='headings', yscrollcommand=scrollbar.set)
            tree.heading('Loan ID', text='Loan ID')
            tree.heading('Account', text='Account Number')
            tree.heading('User Name', text='User Name')
            tree.heading('Amount', text='Loan Amount')
            tree.heading('Status', text='Status')
            
            # Configure scrollbar
            scrollbar.config(command=tree.yview)

            # Store buttons for each loan
            loan_buttons = []

            for loan in loans:
                item = tree.insert('', 'end', values=(
                    loan['id'], 
                    loan['acc_num'], 
                    loan['user_name'], 
                    loan['amount'], 
                    loan['status']
                ))
                
                # Only show approve/reject buttons for pending loans
                if loan['status'] == 'Pending':
                    # Create a frame to hold the buttons
                    button_frame = tk.Frame(loans_window)
                    button_frame.pack(anchor='w', padx=10, pady=5)

                    # Add buttons for each loan
                    approve_btn = ttk.Button(
                        button_frame, 
                        text="Approve", 
                        command=lambda l_id=loan['id'], a_num=loan['acc_num'], amt=loan['amount']: 
                        approve_loan(l_id, a_num, amt)
                    )
                    reject_btn = ttk.Button(
                        button_frame, 
                        text="Reject", 
                        command=lambda l_id=loan['id']: reject_loan(l_id)
                    )
                    
                    # Pack buttons in the frame
                    approve_btn.pack(side=tk.LEFT, padx=5)
                    reject_btn.pack(side=tk.LEFT)

                    # Store buttons to prevent garbage collection
                    loan_buttons.append((button_frame, approve_btn, reject_btn))

            tree.pack(fill='both', expand=True)
            db.close_connection()

        # Admin panel buttons
        buttons = [
            ("View Accounts", view_accounts),
            ("View Transactions", view_transactions),
            ("Manage Loans", manage_loans)
        ]

        for text, command in buttons:
            ttk.Button(admin_window, text=text, command=command).pack(pady=10)

    # Admin Login Window
    admin_login = tk.Toplevel(root)
    admin_login.title("Admin Login")
    admin_login.geometry("300x250")

    tk.Label(admin_login, text="Admin Login", font=("Arial", 16)).pack(pady=10)
    
    tk.Label(admin_login, text="Username:").pack()
    admin_user = ttk.Entry(admin_login)
    admin_user.pack(pady=5)

    tk.Label(admin_login, text="Password:").pack()
    admin_pass = ttk.Entry(admin_login, show="*")
    admin_pass.pack(pady=5)

    ttk.Button(admin_login, text="Login", command=login_admin).pack(pady=10)