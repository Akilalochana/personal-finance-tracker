import json
import tkinter as tk
from tkinter import ttk
import datetime

transactions = {}  # initialize empty dictionary to store transactions

def load_transactions():  # function to load transactions from JSON file
    global transactions  # access the global transactions list
    try:
        with open('PersonalFinanceTraker.json', 'r') as file:  # open the JSON file in read mode
            loaded_data = json.load(file)  # load the data from the file

    except FileNotFoundError:
        print("The file does not exist.")
        transaction = {}  # if file doesn't exist,start an empty file

def save_transactions():  # function to save transactions to JSON file
    global transactions  # access the global transactions list
    with open('PersonalFinanceTraker.json', 'w') as file:  # open the JSON file in write mode
        # write the transactions list to the file
        json.dump(transactions, file, indent=2)


def read_bulk_transactions_from_file(filename):
    global transactions # Access the global transactions dictionary
    filename = input("Enter the file :")
    try:
        filename += ".txt"  # Append the file extension
        with open(filename, "r") as file:  # Open the file in read mode
            for line in file:   # Iterate through each line in the file
                parts = line.strip().split()  # Split the line into parts based on whitespace
                if len(parts) != 4: # Check if the line has exactly 4 parts
                    print("Invalid format in line:", line)
                    continue  # Skip to the next line if the format is invalid
                key, date, description, amount = parts  # Extract the parts from the line
                try:
                    amount = float(amount) # Convert the amount to a floating-point number
                except ValueError:
                    print("Invalid amount format in line:", line)
                    continue   # Skip to the next line if the amount format is invalid
                if key in transactions: # Check if the key already exists in the transactions dictionary
                    transactions[key].append({"amount": amount, "date": date, "description": description})# Append the transaction to the existing key
                else:
                    transactions[key] = [{"amount": amount, "date": date, "description": description}]  # Create a new key and add the transaction
        save_transactions()   # Save the transactions after reading from the file
        print("Bulk transactions read successfully!")
    except FileNotFoundError:
        print("File not found.")


def add_transaction():  # creating a function to add transaction
    global transactions

    while True:   # loop until a valid category is entered
        category = input("Enter the category: ")
        if category.isdigit():  # check if the input id digit
            print("Invalid input, Enter the category correctly")

        else:
            save_transactions()  # save the transactions
            break

    while True:  # loop until a valid category is entered
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a amount.")

    while True:   # loop until a valid category is entered
        transaction_type = input("Enter type (income/expense): ")
        # check if the input is valid transaction type
        if transaction_type.lower() not in ["income", "expense"]:
            print("Invalid input, Please enter a income or expense!")

        else:

            save_transactions()  # save the transactions
            break

    while True:   # loop until a valid category is entered
        date = input("Enter the date(YYYY-MM-DD) :")
        try:
            # Attempt to parse the entered date string into a datetime object
            new_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format, please enter the date in yyyy-MM-DD format.")

    if category not in transactions:  # check if the category is not already in the transactions dictionary
        # if not , creat a empty list for the category
        transactions[category] = []

    # creat a transaction dictionary with the provided amount, transaction type, and date
    transaction = {"amount": (
        amount), "transaction_type": transaction_type, "date": date}
    # append the transactiona to the list Corresponding to the category
    transactions[category].append(transaction)
    save_transactions()  # save the transactions
    print("Transaction added successfully !")


def view_transaction():  # creating a function to view transaction
    global transactions
    print("\n transactions : ")  # display the massage
    if not transactions:
        # if not transactions display a massage
        print("No transactions to display")
    else:

        class FinanceTrackerGUI:
            def __init__(self, root):
                self.root = root
                self.root.title("Personal Finance Tracker")
                self.root.geometry("800x500")
                self.transactions = self.load_transactions("PersonalFinanceTraker.json")
                self.create_widgets()

            def create_widgets(self):
                # create label
                label = ttk.Label(self.root, text="Personal Finance Tracker", font=('Helvetica', 25))
                label.pack()

                # frame for table and scrollbar
                frame = ttk.Frame(self.root, relief=tk.GROOVE)
                frame.pack_propagate(False)
                frame.pack()
                frame.place(x=13, y=160, width=770, height=220)

                # Treeview for displaying transactions
                self.table = ttk.Treeview(frame, columns=("id", "category", "amount", "date"), show='headings')
                self.table.pack()
                self.table.place(width=755, height=220)

                self.table.heading('id', text='Id')
                self.table.heading('category', text='Category', command=lambda: self.sort_by_column('category', False))
                self.table.heading('amount', text='Amount', command=lambda: self.sort_by_column('amount', False))
                self.table.heading('date', text='Date', command=lambda: self.sort_by_column('date', False))

                self.table.column('id', width=50)
                self.table.column('amount', width=100)

                # scrollbar for the treeview
                scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL)
                scroll_y.pack(side='right', fill='y')
                self.table.configure(yscrollcommand=scroll_y.set)

                # search bar and buttons
                self.var_search = tk.StringVar()
                lbl_search_panel = ttk.Label(self.root, text="Search by category", font=('Helvetica', 12))
                lbl_search_panel.place(x=10, y=90)

                txt_search_panel = ttk.Entry(self.root, textvariable=self.var_search)
                txt_search_panel.place(x=155, y=90, width=400, height=25)

                button = ttk.Button(self.root, text="Search", command=self.search_transactions)
                button.place(x=560, y=90, width=100, height=27)

                button_refresh = ttk.Button(self.root, text="Refresh", command=self.refresh_table)
                button_refresh.place(x=670, y=90, width=100, height=27)

                # Display transactions initially
                self.display_transactions(self.transactions)


            def sort_by_column(self, col, reverse):
                # Get the items and sort them
                data = [(self.table.set(item, col), item) for item in self.table.get_children('')]
                data.sort(reverse=reverse)

                # Rearrange items in the treeview based on the sorted order
                for index, (val, item) in enumerate(data):
                    self.table.move(item, '', index)


            def load_transactions(self, filename):
                with open(filename, 'r') as file:
                    data = json.load(file)
                return data
                            
            def display_transactions(self, transactions):
                for row in self.table.get_children():
                    self.table.delete(row)
                index = 1 # Global index counter
                for category, entries in transactions.items():
                    for entry in entries:
                        amount = entry['amount']
                        date = entry['date']
                        self.table.insert('', 'end', values=(index, category, amount, date))
                        index += 1 # increment the global index counter

            def search_transactions(self):
                search_category = self.var_search.get().lower()  # Get search query from the entry widget
                filtered_transactions ={}
                for category, entries in self.transactions.items():
                    if search_category in category.lower():
                        filtered_transactions[category] = entries
                self.display_transactions(filtered_transactions)

            def refresh_table(self):
                self.display_transactions(self.transactions)

            
        def main():
            root = tk.Tk()
            app = FinanceTrackerGUI(root)
            app.display_transactions(app.transactions)
            root.mainloop()

        if __name__=="__main__":
            main()    


def update_transaction():  # creating a function to update transactions
    global transactions  # access the global transactions list
    view_transaction()  # call view transactions to display all transactions
    if not transactions:  # if not transactions return to print no transactions to display
        return

    # Prompt the user to enter the category they want to update
    category_name = input("Enter the category you want to update :")
    if category_name in transactions:  # Check if the entered category exists in the transactions dictionary

        while True:  # Check if the entered category exists in the transactions dictionary
            try:
                # Prompt the user to enter the amount for the transaction
                amount = float(input("Enter the amount: "))

                break  # Break the loop if a valid amount is entered
            except ValueError:
                # Print an error message
                print("Invalid input. Please enter a amount.")

        while True:  # Begin a loop to handle input for the transaction type

            # Prompt the user to enter the transaction type (income/expense)
            transaction_type = input("Enter type (income/expense): ")
            # Check if the entered transaction type is valid
            if transaction_type.lower() not in ["income", "expense"]:
                print("Invalid input, Please enter a income or expense!")
            else:
                save_transactions()  # save the transactions
                break

        while True:   # Begin a loop to handle input for the transaction date
            # Prompt the user to enter the transaction date in the format YYYY-MM-DD
            date = input("Enter the date(YYYY-MM-DD) :")
            try:
                # Attempt to parse the entered date string into a datetime object
                new_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                break  # Break the loop if the date is entered in the correct format
            except ValueError:
                print("Invalid date format, please enter the date in yyyy-MM-DD format.")

        transactions[category_name] = [{"amount": (
            amount), "transaction_type": transaction_type, "date": date}]  # update the transactions
        save_transactions()  # save the transactions
        print("Transaction updated successfully !")  # display the massage

    else:
        # if the index is not within the range of transactions then this massage will be printed
        print("No such category exists, enter exists category!")


def delete_transaction():  # creating a function to delete transactions
    global transactions  # access the global transactions list
    view_transaction()  # call view transactions to display all transactions
    if not transactions:  # if not transactions return to print no transactions to display
        return

    delete_category = input("Enter the category you want to delete :")

    if delete_category in transactions:
        del transactions[delete_category]
        save_transactions()  # save the transactions
        print("Transaction deleted successfully !")  # display the massage
    else:
        # if the index is not within the range of transactions then this massage will be printed
        print("No such category exists, enter exists category!")
        return


def display_summary():  # creating a function to display transactions
    global transactions  # access the global transactions list
    load_transactions()
    if not transactions:  # if transactions is empty, display No transactions added yet,add transactions
        print("No transactions added yet,add transactions")
        return

    income_list = []  # initialize an empty list to store income amounts
    expense_list = []  # initialize an empty list to store expense amounts

    # Iterate over each category and its transactions in the transactions dictionary
    for category, transactions_list in transactions.items():
        for transaction in transactions_list:

            # Get the amount of the transaction, defaulting to 0 if the amount key is missing
            amount = transaction.get("amount", 0)
            # Check if the transaction type is 'income' and add the amount to the income list
            if transaction.get("transaction_type", "").lower() == "income":
                income_list.append(amount)
            # Check if the transaction type is 'expense' and add the amount to the expense list
            elif transaction.get("transaction_type", "").lower() == "expense":
                expense_list.append(amount)

    print("Your incomes :", income_list)  # Print the list of incomes
    print("your expenses :", expense_list)  # Print the list of expenses
    # Calculate the total income and total expense
    total_income = sum(income_list)
    total_expense = sum(expense_list)

    # Print the total income, total expense, and net balance
    print("Total Income :", total_income)
    print("Total Expense :", total_expense)
    print("Net Balance :", total_income - total_expense)


def main_menu():
    load_transactions()  # load the transactions
    while True:  # infinite loop to keep the program running until exited
        print("\n ---Personal Finance Tracker---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Loaded Transaction")
        print("7. Exit")
        # print the user for their choice
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()  # add a new transaction
        elif choice == '2':
            view_transaction()  # view all the transactions
        elif choice == '3':
            update_transaction()  # update transactions
        elif choice == '4':
            delete_transaction()  # delete transactions
        elif choice == '5':
            display_summary()# display the summary of transactions
        elif choice == '6':
            read_bulk_transactions_from_file(filename ="filename")  
        elif choice == '7':
            print("Exiting program.")
            break  # exit the program
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":  # check the code is begin run
    main_menu()  # call the main_menu function to start the program
