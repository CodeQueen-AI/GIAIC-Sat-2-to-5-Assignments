import json
import questionary
from rich.console import Console
from rich.table import Table
from datetime import datetime

# Initialize Rich Console
console = Console()

# --- Configuration ---
TRANSACTIONS_FILE = "database/transactions.txt"
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]

# --- Utility Functions ---
def load_transactions():
    """Loads transactions from the file."""
    try:
        with open(TRANSACTIONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_transactions(transactions):
    """Saves transactions to the file."""
    with open(TRANSACTIONS_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

# --- Core Features ---
def add_transaction():
    """Adds a new transaction (expense or income)."""
    transaction_type = questionary.select(
        "What type of transaction?",
        choices=["Expense", "Income"]
    ).ask()

    if transaction_type == "Expense":
        category = questionary.select("Select expense category:", choices=EXPENSE_CATEGORIES).ask()
    else:
        category = questionary.select("Select income category:", choices=INCOME_CATEGORIES).ask()

    amount_str = questionary.text(
        "Enter the amount:",
        validate=lambda text: text.replace('.', '', 1).isdigit() or "Please enter a valid number."
    ).ask()
    amount = int(float(amount_str) * 100)  # Store as cents/paisa

    description = questionary.text("Enter a description:").ask()
    date = datetime.now().strftime("%Y-%m-%d")

    transaction = {
        "date": date,
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description
    }

    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)

    console.print("[bold green]Transaction added successfully![/bold green]")

def view_transactions():
    """Displays all transactions in a table."""
    transactions = load_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    table = Table(title="All Transactions")
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Category", style="yellow")
    table.add_column("Amount", justify="right", style="green")
    table.add_column("Description", style="white")

    for t in sorted(transactions, key=lambda i: i['date'], reverse=True):
        amount_display = f"Rs {t['amount'] / 100:.2f}"
        row_style = "red" if t['type'] == 'Expense' else "green"
        table.add_row(
            t['date'],
            t['type'],
            t['category'],
            amount_display,
            t['description'],
            style=row_style
        )

    console.print(table)

def main():
    """Main menu for transaction management."""
    while True:
        choice = questionary.select(
            "Transaction Management",
            choices=["Add Transaction", "View Transactions", "Go Back"]
        ).ask()

        if choice == "Add Transaction":
            add_transaction()
        elif choice == "View Transactions":
            view_transactions()
        elif choice == "Go Back":
            break

if __name__ == "__main__":
    main()