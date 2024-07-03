import tkinter as tk

import sqlite3


def update_label():

    new_text = entry.get()

    label.config(text=new_text)


def add_income():

    amount = entry_income.get()

    name = entry_income_name.get()

    try:

        amount = float(amount)

        current_balance.set(current_balance.get() + amount)

        entry_income.delete(0, tk.END)

        entry_income_name.delete(0, tk.END)

        insert_transaction('income', amount, name)

    except ValueError:

        label.config(text="Invalid input. Please enter a number.")


def add_expense():

    amount = entry_expense.get()

    name = entry_expense_name.get()

    try:

        amount = float(amount)

        current_balance.set(current_balance.get() - amount)

        entry_expense.delete(0, tk.END)

        entry_expense_name.delete(0, tk.END)

        insert_transaction('expense', amount, name)

    except ValueError:

        label.config(text="Invalid input. Please enter a number.")


def delete_transaction():

    transaction_id = entry_delete.get()

    try:

        transaction_id = int(transaction_id)

        remove_transaction(transaction_id)

        entry_delete.delete(0, tk.END)

        load_balance()

    except ValueError:

        label.config(text="Invalid input. Please enter a valid ID.")


def reset_database():

    with sqlite3.connect("finance.db") as conn:

        cursor = conn.cursor()

        cursor.execute("DELETE FROM transactions")

        conn.commit()

    load_balance()


def exit_application():

    root.destroy()


def insert_transaction(transaction_type, amount, name):

    with sqlite3.connect("finance.db") as conn:

        cursor = conn.cursor()

        cursor.execute("INSERT INTO transactions (type, amount, name) VALUES (?, ?, ?)",

                       (transaction_type, amount, name))

        conn.commit()


def remove_transaction(transaction_id):

    with sqlite3.connect("finance.db") as conn:

        cursor = conn.cursor()

        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

        conn.commit()


def create_table():

    with sqlite3.connect("finance.db") as conn:

        cursor = conn.cursor()

        cursor.execute('''

            CREATE TABLE IF NOT EXISTS transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                type TEXT NOT NULL,

                amount REAL NOT NULL,

                name TEXT NOT NULL

            )

        ''')

        conn.commit()


def load_balance():

    with sqlite3.connect("finance.db") as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")

        transactions = cursor.fetchall()

        balance = 0.0

        for transaction in transactions:

            if transaction[0] == 'income':

                balance += transaction[1]

            elif transaction[0] == 'expense':

                balance -= transaction[1]

        current_balance.set(balance)


def view_transactions():
    try:
        with sqlite3.connect("finance.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type, amount, name FROM transactions")
            transactions = cursor.fetchall()

        transaction_window = tk.Toplevel(root)
        transaction_window.title("Transaction History")

        for idx, view_transaction in enumerate(transactions):
            transaction_label = tk.Label(transaction_window, text=f"{view_transactions[0]}. {view_transactions[1]} - {view_transactions[3]}: ${view_transactions[2]:.2f}")
            transaction_label.pack()

    except sqlite3.Error as e:
        print(f"Error fetching transactions: {e}")


def search_transactions():

    search_term = entry_search.get()

    with sqlite3.connect("finance.db") as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT id, type, amount, name FROM transactions WHERE type LIKE ? OR name LIKE ?",

                       ('%' + search_term + '%', '%' + search_term + '%'))

        transactions = cursor.fetchall()

    # Create a new window

    search_window = tk.Toplevel(root)

    search_window.title("Search Results")
    # Display search results in the new window
for idx, transaction in enumerate(transactions):
    transaction_label = tk.Label(transaction_window, text=f"{transaction[0]}. {transaction[1]} - {transaction[3]}: ${transaction[2]:.2f}")
    transaction_label.pack()


# Create the main window
root = tk.Tk()
root.title("Finance App")

# Create a label frame for balance
balance_frame = tk.LabelFrame(root, text="Balance")
balance_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

# Current balance label
current_balance = tk.DoubleVar(value=0.0)
balance_label = tk.Label(balance_frame, textvariable=current_balance)
balance_label.pack(pady=10)

# Create a label frame for income
income_frame = tk.LabelFrame(root, text="Add Income")
income_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

# Entry and button for income
income_label = tk.Label(income_frame, text="Amount:")
income_label.grid(row=0, column=0, pady=5, padx=5)
entry_income = tk.Entry(income_frame)
entry_income.grid(row=0, column=1, pady=5, padx=5)
income_name_label = tk.Label(income_frame, text="Name:")
income_name_label.grid(row=1, column=0, pady=5, padx=5)
entry_income_name = tk.Entry(income_frame)
entry_income_name.grid(row=1, column=1, pady=5, padx=5)
button_income = tk.Button(income_frame, text="Add Income", command=add_income)
button_income.grid(row=2, column=0, columnspan=2, pady=5)

# Create a label frame for expense
expense_frame = tk.LabelFrame(root, text="Add Expense")
expense_frame.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")

# Entry and button for expense
expense_label = tk.Label(expense_frame, text="Amount:")
expense_label.grid(row=0, column=0, pady=5, padx=5)
entry_expense = tk.Entry(expense_frame)
entry_expense.grid(row=0, column=1, pady=5, padx=5)
expense_name_label = tk.Label(expense_frame, text="Name:")
expense_name_label.grid(row=1, column=0, pady=5, padx=5)
entry_expense_name = tk.Entry(expense_frame)
entry_expense_name.grid(row=1, column=1, pady=5, padx=5)
button_expense = tk.Button(expense_frame, text="Add Expense", command=add_expense)
button_expense.grid(row=2, column=0, columnspan=2, pady=5)

# Create a label frame for deleting transactions
delete_frame = tk.LabelFrame(root, text="Delete Transaction")
delete_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

# Entry and button to delete transaction
delete_label = tk.Label(delete_frame, text="Transaction ID:")
delete_label.grid(row=0, column=0, pady=5, padx=5)
entry_delete = tk.Entry(delete_frame)
entry_delete.grid(row=0, column=1, pady=5, padx=5)
button_delete = tk.Button(delete_frame, text="Delete Transaction", command=delete_transaction)
button_delete.grid(row=1, column=0, columnspan=2, pady=5)

# Create a label frame for searching transactions
search_frame = tk.LabelFrame(root, text="Search Transactions")
search_frame.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

# Entry and button to search transactions
search_label = tk.Label(search_frame, text="Search Term:")
search_label.grid(row=0, column=0, pady=5, padx=5)
entry_search = tk.Entry(search_frame)
entry_search.grid(row=0, column=1, pady=5, padx=5)
button_search = tk.Button(search_frame, text="Search Transactions", command=search_transactions)
button_search.grid(row=1, column=0, columnspan=2, pady=5)

# Buttons for viewing transactions, resetting database, and exiting
view_button = tk.Button(root, text="View Transactions", command=view_transactions)
view_button.grid(row=4, column=0, pady=10, padx=10, sticky="ew")
reset_button = tk.Button(root, text="Reset Database", command=reset_database)
reset_button.grid(row=4, column=1, pady=10, padx=10, sticky="ew")
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.grid(row=4, column=2, pady=10, padx=10, sticky="ew")

# Create the transactions table if it doesn't exist
create_table()

# Load the initial balance
load_balance()

# Run the application
root.mainloop()