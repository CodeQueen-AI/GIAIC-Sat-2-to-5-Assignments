
import json
import csv
import questionary
from rich.console import Console
from pathlib import Path

console = Console()

TRANSACTIONS_FILE = "database/transactions.txt"
BUDGETS_FILE = "database/budgets.txt"

def load_data(file_path):
    """Loads JSON data from a file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def export_transactions_to_csv(transactions, filepath):
    """Exports transactions to a CSV file."""
    if not transactions:
        console.print("[bold yellow]No transactions to export.[/bold yellow]")
        return

    try:
        with open(filepath, 'w', newline='') as f:
            fieldnames = ['date', 'type', 'category', 'amount', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for t in transactions:
                # Convert amount back from paisa/cents for readability in CSV
                t['amount'] = t['amount'] / 100
                writer.writerow(t)
        console.print(f"[bold green]Transactions exported successfully to {filepath}[/bold green]")
    except IOError as e:
        console.print(f"[bold red]Error exporting transactions to CSV: {e}[/bold red]")

def export_budgets_to_csv(budgets, filepath):
    """Exports budgets to a CSV file."""
    if not budgets:
        console.print("[bold yellow]No budgets to export.[/bold yellow]")
        return

    try:
        with open(filepath, 'w', newline='') as f:
            fieldnames = ['month', 'category', 'amount']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for b in budgets:
                # Convert amount back from paisa/cents for readability in CSV
                b['amount'] = b['amount'] / 100
                writer.writerow(b)
        console.print(f"[bold green]Budgets exported successfully to {filepath}[/bold green]")
    except IOError as e:
        console.print(f"[bold red]Error exporting budgets to CSV: {e}[/bold red]")

def export_data():
    """Guides the user through exporting data."""
    export_type = questionary.select(
        "What data would you like to export?",
        choices=["Transactions", "Budgets", "Both"]
    ).ask()

    file_format = questionary.select(
        "Select export format:",
        choices=["CSV", "JSON"]
    ).ask()

    output_filename = questionary.text(
        "Enter output filename (e.g., my_transactions):"
    ).ask()

    output_path = Path.cwd() / f"{output_filename}.{file_format.lower()}"

    transactions = load_data(TRANSACTIONS_FILE)
    budgets = load_data(BUDGETS_FILE)

    if export_type == "Transactions" or export_type == "Both":
        if file_format == "CSV":
            export_transactions_to_csv(transactions, output_path.with_name(f'{output_filename}_transactions.csv'))
        else:
            # JSON export
            with open(output_path.with_name(f'{output_filename}_transactions.json'), 'w') as f:
                json.dump(transactions, f, indent=4)
            console.print(f"[bold green]Transactions exported successfully to {output_path.with_name(f'{output_filename}_transactions.json')}[/bold green]")

    if export_type == "Budgets" or export_type == "Both":
        if file_format == "CSV":
            export_budgets_to_csv(budgets, output_path.with_name(f'{output_filename}_budgets.csv'))
        else:
            # JSON export
            with open(output_path.with_name(f'{output_filename}_budgets.json'), 'w') as f:
                json.dump(budgets, f, indent=4)
            console.print(f"[bold green]Budgets exported successfully to {output_path.with_name(f'{output_filename}_budgets.json')}[/bold green]")

def clear_all_data():
    """Clears all transaction and budget data after confirmation."""
    confirmation = questionary.confirm(
        "[bold red]WARNING:[/bold red] This will permanently delete ALL your transaction and budget data. Are you sure you want to proceed?"
    ).ask()

    if confirmation:
        # Clear transactions
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump([], f)
        # Clear budgets
        with open(BUDGETS_FILE, 'w') as f:
            json.dump([], f)
        console.print("[bold green]All financial data has been cleared.[/bold green]")
    else:
        console.print("[bold yellow]Data clearing cancelled.[/bold yellow]")

def main():
    """Main menu for data management."""
    while True:
        choice = questionary.select(
            "Data Management",
            choices=["Export Data", "Clear All Data", "Go Back"]
        ).ask()

        if choice == "Export Data":
            export_data()
        elif choice == "Clear All Data":
            clear_all_data()
        elif choice == "Go Back":
            break

if __name__ == "__main__":
    main()
