import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Create or connect to a SQLite database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create a table for expenses if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        description TEXT,
        amount REAL
    )
''')
conn.commit()

# Function to add an expense
def add_expense():
    description = description_entry.get()
    amount = amount_entry.get()

    if description and amount:
        try:
            amount_value = float(amount)
            if amount_value < 0:
                raise ValueError
            c.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)', (description, amount_value))
            conn.commit()
            description_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
            load_expenses()
            calculate_total()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive amount.")
    else:
        messagebox.showerror("Input Error", "Please fill out all fields.")

# Function to load expenses from the database with sorting
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    # Retrieve selected sorting option
    sort_by = sort_by_var.get()
    order_column = {
        "ID": "id",
        "Description": "description",
        "Amount": "amount"
    }.get(sort_by, "id")  # Default to "id" if no valid option is selected

    c.execute(f'SELECT * FROM expenses ORDER BY {order_column} ASC')
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)

    calculate_total()  # Calculate total after loading expenses

# Function to delete selected expense
def delete_expense():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        expense_id = item['values'][0]
        c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        load_expenses()
    else:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")

# Function to calculate the total expenses
def calculate_total():
    c.execute('SELECT SUM(amount) FROM expenses')
    total = c.fetchone()[0] or 0
    total_label.config(text=f"Total Expenses: ${total:.2f}")

# Function to search expenses
def search_expenses():
    search_term = search_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    
    c.execute('SELECT * FROM expenses WHERE description LIKE ?', ('%' + search_term + '%',))
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)

# Create the main window
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("600x550")
root.configure(bg="#E8F0F2")

# Create frames for better organization
input_frame = tk.Frame(root, bg="#E8F0F2")
input_frame.pack(pady=10)

tree_frame = tk.Frame(root, bg="#E8F0F2")
tree_frame.pack(pady=10)

button_frame = tk.Frame(root, bg="#E8F0F2")
button_frame.pack(pady=10)

search_frame = tk.Frame(root, bg="#E8F0F2")
search_frame.pack(pady=10)

sort_frame = tk.Frame(root, bg="#E8F0F2")
sort_frame.pack(pady=10)

# Create input fields
tk.Label(input_frame, text="Description", bg="#E8F0F2", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
description_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
description_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Amount", bg="#E8F0F2", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

# Add button
add_button = tk.Button(button_frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white", font=("Arial", 12))
add_button.grid(row=0, column=0, padx=10)

# Create a Treeview to display expenses
columns = ('ID', 'Description', 'Amount')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
tree.heading('ID', text='ID')
tree.heading('Description', text='Description')
tree.heading('Amount', text='Amount')
tree.column("ID", width=50)
tree.column("Description", width=250)
tree.column("Amount", width=100)
tree.grid(row=0, column=0)

# Total Expenses Label
total_label = tk.Label(root, text="Total Expenses: $0.00", bg="#E8F0F2", font=("Arial", 14, "bold"))
total_label.pack(pady=10)

# Delete button
delete_button = tk.Button(button_frame, text="Delete Expense", command=delete_expense, bg="#f44336", fg="white", font=("Arial", 12))
delete_button.grid(row=0, column=1, padx=10)

# Search field
tk.Label(search_frame, text="Search:", bg="#E8F0F2", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame, font=("Arial", 12), width=20)
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=search_expenses, bg="#2196F3", fg="white", font=("Arial", 12))
search_button.pack(side=tk.LEFT, padx=5)

# Sorting dropdown
sort_by_var = tk.StringVar(value="ID")  # Default sorting option
tk.Label(sort_frame, text="Sort by:", bg="#E8F0F2", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
sort_dropdown = ttk.Combobox(sort_frame, textvariable=sort_by_var, values=["ID", "Description", "Amount"], state="readonly", font=("Arial", 12))
sort_dropdown.pack(side=tk.LEFT, padx=5)
sort_dropdown.bind("<<ComboboxSelected>>", lambda event: load_expenses())

# Load existing expenses
load_expenses()

# Run the application
root.mainloop()

# Close the database connection when done
conn.close()
