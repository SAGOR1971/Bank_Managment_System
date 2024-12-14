import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection

def user_dashboard(root, account):
    """
    User Dashboard for managing their account.
    """
    acc_num = account['acc_num']
    user_name = account['user_name']
    balance = account['balance']

    dashboard = tk.Toplevel(root)
    dashboard.title("User Dashboard")
    dashboard.geometry("400x600")

    def check_balance():
        balance_window = tk.Toplevel(dashboard)
        balance_window.title("Check Balance")
        balance_window.geometry("300x200")
        tk.Label(balance_window, text=f"Current Balance: {balance} Taka", font=("Arial", 14)).pack(pady=20)

    def loan_status():
        db = DatabaseConnection()
        loans = db.fetch_all("SELECT * FROM loans WHERE acc_num = %s", (acc_num,))

        loan_status_window = tk.Toplevel(dashboard)
        loan_status_window.title("Loan Status")
        loan_status_window.geometry("400x300")

        # Create Treeview for displaying loans
        tree = ttk.Treeview(loan_status_window, columns=('Loan ID', 'Amount', 'Status'), show='headings')
        tree.heading('Loan ID', text='Loan ID')
        tree.heading('Amount', text='Amount')
        tree.heading('Status', text='Status')

        if loans:
            for loan in loans:
                tree.insert('', 'end', values=(
                    loan['id'], 
                    loan['amount'], 
                    loan['status']
                ))
            tree.pack(fill='both', expand=True, pady=20)
        else:
            tk.Label(loan_status_window, text="No loan applications found", font=("Arial", 12)).pack(pady=20)

        db.close_connection()

    def withdraw():
        def perform_withdraw():
            db = DatabaseConnection()
            amount = withdraw_entry.get()

            if amount.isdigit():
                amount = float(amount)
                current_balance = db.fetch_one("SELECT balance FROM accounts WHERE acc_num = %s", (acc_num,))['balance']

                if current_balance >= amount:
                    db.execute_query("UPDATE accounts SET balance = balance - %s WHERE acc_num = %s", (amount, acc_num))
                    db.execute_query(
                        "INSERT INTO transactions (acc_num, transaction_date, amount, type) VALUES (%s, NOW(), %s, 'withdraw')",
                        (acc_num, -amount)
                    )
                    messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
                    withdraw_window.destroy()
                else:
                    messagebox.showerror("Error", "Insufficient balance!")
            else:
                messagebox.showerror("Error", "Invalid amount")

            db.close_connection()

        withdraw_window = tk.Toplevel(dashboard)
        withdraw_window.title("Withdraw Money")
        withdraw_window.geometry("300x200")

        tk.Label(withdraw_window, text="Enter Amount to Withdraw:", font=("Arial", 12)).pack(pady=10)
        withdraw_entry = ttk.Entry(withdraw_window)
        withdraw_entry.pack(pady=10)
        ttk.Button(withdraw_window, text="Withdraw", command=perform_withdraw).pack(pady=10)

    def deposit():
        def perform_deposit():
            db = DatabaseConnection()
            amount = deposit_entry.get()

            if amount.isdigit():
                amount = float(amount)
                db.execute_query("UPDATE accounts SET balance = balance + %s WHERE acc_num = %s", (amount, acc_num))
                db.execute_query(
                    "INSERT INTO transactions (acc_num, transaction_date, amount, type) VALUES (%s, NOW(), %s, 'deposit')",
                    (acc_num, amount)
                )
                messagebox.showinfo("Success", f"Deposited {amount} successfully!")
                deposit_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid amount")

            db.close_connection()

        deposit_window = tk.Toplevel(dashboard)
        deposit_window.title("Deposit Money")
        deposit_window.geometry("300x200")

        tk.Label(deposit_window, text="Enter Amount to Deposit:", font=("Arial", 12)).pack(pady=10)
        deposit_entry = ttk.Entry(deposit_window)
        deposit_entry.pack(pady=10)
        ttk.Button(deposit_window, text="Deposit", command=perform_deposit).pack(pady=10)

    def fund_transfer():
        def perform_transfer():
            db = DatabaseConnection()
            recipient_acc = recipient_entry.get()
            amount = transfer_entry.get()

            if amount.isdigit() and recipient_acc.isdigit():
                amount = float(amount)
                recipient = db.fetch_one("SELECT * FROM accounts WHERE acc_num = %s", (recipient_acc,))

                if recipient:
                    current_balance = db.fetch_one("SELECT balance FROM accounts WHERE acc_num = %s", (acc_num,))['balance']

                    if current_balance >= amount:
                        db.execute_query("UPDATE accounts SET balance = balance - %s WHERE acc_num = %s", (amount, acc_num))
                        db.execute_query("UPDATE accounts SET balance = balance + %s WHERE acc_num = %s", (amount, recipient_acc))
                        db.execute_query(
                            "INSERT INTO transactions (acc_num, transaction_date, amount, type) VALUES (%s, NOW(), %s, 'transfer')",
                            (acc_num, -amount)
                        )
                        db.execute_query(
                            "INSERT INTO transactions (acc_num, transaction_date, amount, type) VALUES (%s, NOW(), %s, 'transfer')",
                            (recipient_acc, amount)
                        )
                        messagebox.showinfo("Success", f"Transferred {amount} to {recipient_acc} successfully!")
                        transfer_window.destroy()
                    else:
                        messagebox.showerror("Error", "Insufficient balance!")
                else:
                    messagebox.showerror("Error", "Recipient account not found!")
            else:
                messagebox.showerror("Error", "Invalid amount or account number")

            db.close_connection()

        transfer_window = tk.Toplevel(dashboard)
        transfer_window.title("Fund Transfer")
        transfer_window.geometry("400x300")

        tk.Label(transfer_window, text="Enter Recipient Account Number:", font=("Arial", 12)).pack(pady=10)
        recipient_entry = ttk.Entry(transfer_window)
        recipient_entry.pack(pady=10)

        tk.Label(transfer_window, text="Enter Amount to Transfer:", font=("Arial", 12)).pack(pady=10)
        transfer_entry = ttk.Entry(transfer_window)
        transfer_entry.pack(pady=10)

        ttk.Button(transfer_window, text="Transfer", command=perform_transfer).pack(pady=10)

    def apply_loan():
        def perform_apply():
            db = DatabaseConnection()
            amount = loan_entry.get()

            if amount.isdigit():
                amount = float(amount)
                # Ensure only one active loan per account
                existing_loan = db.fetch_one("SELECT * FROM loans WHERE acc_num = %s AND status = 'Pending'", (acc_num,))
                
                if existing_loan:
                    messagebox.showerror("Error", "You already have a pending loan application!")
                else:
                    db.execute_query(
                        "INSERT INTO loans (acc_num, amount, status, application_date) VALUES (%s, %s, 'Pending', NOW())",
                        (acc_num, amount)
                    )
                    messagebox.showinfo("Success", f"Loan application for {amount} submitted successfully!")
                    loan_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid amount")

            db.close_connection()

        loan_window = tk.Toplevel(dashboard)
        loan_window.title("Apply for Loan")
        loan_window.geometry("300x200")

        tk.Label(loan_window, text="Enter Loan Amount:", font=("Arial", 12)).pack(pady=10)
        loan_entry = ttk.Entry(loan_window)
        loan_entry.pack(pady=10)
        ttk.Button(loan_window, text="Apply", command=perform_apply).pack(pady=10)

    tk.Label(dashboard, text=f"Welcome, {user_name}!", font=("Arial", 18)).pack(pady=20)
    tk.Label(dashboard, text=f"Current Balance: {balance}", font=("Arial", 14)).pack(pady=10)

    buttons = [
        ("Check Balance", check_balance),
        ("Check Loan Status", loan_status),
        ("Withdraw", withdraw),
        ("Deposit", deposit),
        ("Fund Transfer", fund_transfer),
        ("Apply for Loan", apply_loan)
    ]

    for text, command in buttons:
        ttk.Button(dashboard, text=text, command=command).pack(pady=10)