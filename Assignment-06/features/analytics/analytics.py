# Analytics feature implementation
import questionary
import json
from datetime import datetime, timedelta
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

TRANSACTIONS_FILE = "database/transactions.txt"
BUDGETS_FILE = "database/budgets.txt" # Needed for financial health score, not directly for spending analysis but good to include

def load_transactions():
    """Loads transactions from the file."""
    try:
        with open(TRANSACTIONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_monthly_transactions(transactions, year_month):
    """Filters transactions for a specific YYYY-MM."""
    return [t for t in transactions if t['date'].startswith(year_month)]

def get_expenses_by_category(transactions):
    """Aggregates expenses by category."""
    expenses_by_category = defaultdict(int)
    for t in transactions:
        if t['type'] == 'Expense':
            expenses_by_category[t['category']] += t['amount']
    return expenses_by_category

def calculate_total_expenses(transactions):
    """Calculates total expenses for a list of transactions."""
    return sum(t['amount'] for t in transactions if t['type'] == 'Expense')

def calculate_total_income(transactions):
    """Calculates total income for a list of transactions."""
    return sum(t['amount'] for t in transactions if t['type'] == 'Income')

def get_month_range(year_month):
    """Returns the start and end date of a given YYYY-MM as datetime objects."""
    start_date = datetime.strptime(year_month, "%Y-%m").date()
    # Go to the next month and subtract one day to get the last day of the current month
    end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    return start_date, end_date

def spending_analysis():
    """Performs and displays spending analysis."""
    transactions = load_transactions()
    if not transactions:
        console.print("[bold yellow]No transactions available for analysis.[/bold yellow]")
        return

    today = datetime.now()
    current_month_str = today.strftime("%Y-%m")
    last_month_str = (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    current_month_transactions = get_monthly_transactions(transactions, current_month_str)
    last_month_transactions = get_monthly_transactions(transactions, last_month_str)

    # --- Spending Breakdown by Category (Current Month) ---
    console.print(f"\n[bold underline]Spending Breakdown for {current_month_str}:[/bold underline]")
    current_month_expenses_by_category = get_expenses_by_category(current_month_transactions)
    total_current_month_expenses = calculate_total_expenses(current_month_transactions)

    if not current_month_expenses_by_category:
        console.print("[yellow]No expenses recorded for this month.[/yellow]")
    else:
        # ASCII Pie Chart
        console.print("[bold cyan]Spending by Category:[/bold cyan]")
        for category, amount in sorted(current_month_expenses_by_category.items(), key=lambda item: item[1], reverse=True):
            percentage = (amount / total_current_month_expenses) * 100 if total_current_month_expenses > 0 else 0
            bar_length = int(percentage / 2) # Max 50 chars for the bar
            console.print(f"{category.ljust(12)} {'█' * bar_length} {percentage:.0f}% (Rs {amount/100:.2f})")

        # Top 3 Spending Categories
        sorted_categories = sorted(current_month_expenses_by_category.items(), key=lambda item: item[1], reverse=True)
        console.print("\n[bold magenta]Top 3 Spending Categories:[/bold magenta]")
        for i, (category, amount) in enumerate(sorted_categories[:3]):
            console.print(f"  {i+1}. {category}: Rs {amount/100:.2f}")

    # --- Average Daily Expense (Current Month) ---
    if current_month_transactions:
        start_date, end_date = get_month_range(current_month_str)
        num_days_in_month = (end_date - start_date).days + 1
        days_passed = (today.date() - start_date).days + 1
        
        # Calculate average daily expense based on days passed so far this month
        avg_daily_expense = (total_current_month_expenses / days_passed) if days_passed > 0 else 0
        console.print(f"\n[bold green]Average Daily Expense (this month):[/bold green] Rs {avg_daily_expense/100:.2f}")

    # --- Comparison with Last Month ---
    total_last_month_expenses = calculate_total_expenses(last_month_transactions)
    console.print(f"\n[bold underline]Spending Comparison:[/bold underline]")
    console.print(f"  [cyan]{current_month_str} Expenses:[/cyan] Rs {total_current_month_expenses/100:.2f}")
    console.print(f"  [cyan]{last_month_str} Expenses:[/cyan]  Rs {total_last_month_expenses/100:.2f}")

    if total_last_month_expenses > 0:
        change = total_current_month_expenses - total_last_month_expenses
        percentage_change = (change / total_last_month_expenses) * 100
        change_text = f"Rs {abs(change)/100:.2f}"
        if change > 0:
            console.print(f"  [bold red]  ↑ Increased by {change_text} ({percentage_change:.2f}%)[/bold red]")
        elif change < 0:
            console.print(f"  [bold green]  ↓ Decreased by {change_text} ({abs(percentage_change):.2f}%)[/bold green]")
        else:
            console.print("[bold white]  No significant change.[/bold white]")
    else:
        if total_current_month_expenses > 0:
            console.print(f"  [bold green]  Spending started this month.[/bold green]")
        else:
            console.print("[bold white]  No expenses in both months.[/bold white]")


def main():
    """Main menu for financial analytics."""
    while True:
        choice = questionary.select(
            "Financial Analytics",
            choices=["Spending Analysis", "Income Analysis (Coming Soon)", "Savings Analysis (Coming Soon)", "Financial Health Score (Coming Soon)", "Generate Report (Coming Soon)", "Go Back"]
        ).ask()

        if choice == "Spending Analysis":
            spending_analysis()
        elif choice == "Go Back":
            break
        else:
            console.print("[bold yellow]This feature is coming soon![/bold yellow]")

if __name__ == "__main__":
    main()