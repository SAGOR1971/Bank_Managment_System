import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from database import DatabaseConnection

def new_account(root):
    """
    GUI for creating a new account.
    """
    new_account_window = tk.Toplevel(root)
    new_account_window.title("Create New Account")
    new_account_window.geometry("700x600")

    # Entry variables
    ent_name = ttk.Entry(new_account_window, width=30)
    ent_address = ttk.Entry(new_account_window, width=30)
    ent_phone = ttk.Entry(new_account_window, width=30)
    ent_email = ttk.Entry(new_account_window, width=30)
    ent_dob_year = ttk.Entry(new_account_window, width=30)
    ent_dob_month = ttk.Entry(new_account_window, width=10)
    ent_dob_day = ttk.Entry(new_account_window, width=10)
    initial_deposit_entry = ttk.Entry(new_account_window, width=30)

    # Account type radio buttons
    acctype = StringVar(value="Savings")

    def create_account():
        """
        Create a new account with an initial deposit.
        """
        name = ent_name.get()
        address = ent_address.get()
        phone = ent_phone.get()
        acc_type = acctype.get()
        email = ent_email.get()
        dob = f"{ent_dob_year.get()}-{ent_dob_month.get()}-{ent_dob_day.get()}"
        initial_deposit = initial_deposit_entry.get()

        # Input validation
        if not all([name, address, phone, email, dob, initial_deposit]):
            messagebox.showerror("Error", "All fields are required")
            return

        if not initial_deposit.isdigit():
            messagebox.showerror("Error", "Invalid initial deposit amount")
            return

        initial_deposit = float(initial_deposit)
        acc_num = "880" + phone

        db = DatabaseConnection()
        try:
            # Insert account details
            db.execute_query(
                "INSERT INTO accounts (acc_num, user_name, address, phone, acc_type, email, balance, dob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (acc_num, name, address, phone, acc_type, email, initial_deposit, dob)
            )

            # Insert initial transaction
            db.execute_query(
                "INSERT INTO transactions (acc_num, transaction_date, amount, type) VALUES (%s, NOW(), %s, 'deposit')",
                (acc_num, initial_deposit)
            )

            messagebox.showinfo("Success", f"Account created successfully!\nAccount Number: {acc_num}")
            new_account_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            db.close_connection()

    # Layout
    tk.Label(new_account_window, text="                    Create New Account", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Name Field
    tk.Label(new_account_window, text="Name:").grid(row=1, column=0, pady=5, sticky="e")
    ent_name.grid(row=1, column=1, pady=5)

    # Address Field
    tk.Label(new_account_window, text="Address:").grid(row=2, column=0, pady=5, sticky="e")
    ent_address.grid(row=2, column=1, pady=5)

    # Phone Field
    tk.Label(new_account_window, text="Phone:").grid(row=3, column=0, pady=5, sticky="e")
    ent_phone.grid(row=3, column=1, pady=5)

    # Account Type Radio Buttons
    tk.Label(new_account_window, text="Account Type:").grid(row=4, column=0, pady=5, sticky="e")
    ttk.Radiobutton(new_account_window, text="Savings", variable=acctype, value="Savings").grid(row=4, column=1, sticky="w")
    ttk.Radiobutton(new_account_window, text="Current", variable=acctype, value="Current").grid(row=5, column=1, sticky="w")

    # Email Field
    tk.Label(new_account_window, text="Email:").grid(row=6, column=0, pady=5, sticky="e")
    ent_email.grid(row=6, column=1, pady=5)

    # Date of Birth Field
    tk.Label(new_account_window, text="Date of Birth (YYYY-MM-DD):").grid(row=7, column=0, pady=5, sticky="e")
    ent_dob_year.grid(row=7, column=1, padx=5, sticky="w")
    tk.Label(new_account_window, text="-").grid(row=7, column=2, sticky="w")
    ent_dob_month.grid(row=7, column=3, padx=5, sticky="w")
    tk.Label(new_account_window, text="-").grid(row=7, column=4, sticky="w")
    ent_dob_day.grid(row=7, column=5, padx=5, sticky="w")

    # Initial Deposit Field
    tk.Label(new_account_window, text="Initial Deposit:").grid(row=8, column=0, pady=5, sticky="e")
    initial_deposit_entry.grid(row=8, column=1, pady=5)

    # Create Account Button
    ttk.Button(new_account_window, text="Create Account", command=create_account).grid(row=9, column=0, columnspan=2, pady=20)

    new_account_window.mainloop()
