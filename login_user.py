import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection
from user_dashboard import user_dashboard

def login_user(root):
    """
    User login functionality.
    """
    def verify_user():
        acc_num = login_entry.get()
        db = DatabaseConnection()
        
        query = "SELECT * FROM accounts WHERE acc_num = %s"
        account = db.fetch_one(query, (acc_num,))

        if account:
            login_window.destroy()
            user_dashboard(root, account)  # Open user dashboard
        else:
            messagebox.showerror("Error", "Invalid Account Number")
        
        db.close_connection()

    login_window = tk.Toplevel(root)
    login_window.title("User Login")
    login_window.geometry("300x200")
    
    tk.Label(login_window, text="Enter Account Number:", font=("Arial", 12)).pack(pady=10)
    login_entry = ttk.Entry(login_window, font=("Arial", 12))
    login_entry.pack(pady=10)
    
    ttk.Button(login_window, text="Login", command=verify_user).pack(pady=10)