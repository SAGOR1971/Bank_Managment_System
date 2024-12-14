import tkinter as tk
from tkinter import ttk

from create_account import new_account
from login_user import login_user
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard

class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("400x500")
        
        self.create_main_screen()

    def create_main_screen(self):
        # Main title
        tk.Label(
            self.root, 
            text='Bank Management System', 
            font=('Arial', 20, 'bold')
        ).pack(pady=20)

        # Button styling
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)

        # Main screen buttons
        buttons = [
            ("Create New Account", self.open_new_account),
            ("User Login", self.open_user_login),
            ("Admin Dashboard", self.open_admin_dashboard)
        ]

        for text, command in buttons:
            ttk.Button(
                self.root, 
                text=text, 
                command=command, 
                style='TButton'
            ).pack(pady=10, padx=50, fill='x')

    def open_new_account(self):
        new_account(self.root)

    def open_user_login(self):
        login_user(self.root)

    def open_admin_dashboard(self):
        admin_dashboard(self.root)

def main():
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()