# import json
# import questionary
# from rich.console import Console
# from rich.table import Table
# from rich.progress import Progress, BarColumn, TextColumn, ConsoleColumn
# from datetime import datetime

# # Initialize Rich Console
# console = Console()

# # --- Configuration ---
# BUDGETS_FILE = "database/budgets.txt"
# TRANSACTIONS_FILE = "database/transactions.txt" # Need to read transactions to calculate spent
# EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]

# # --- Utility Functions ---
# def load_budgets():
#     """Loads budgets from the file."""
#     try:
#         with open(BUDGETS_FILE, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def save_budgets(budgets):
#     """Saves budgets to the file."""
#     with open(BUDGETS_FILE, 'w') as f:
#         json.dump(budgets, f, indent=4)

# def load_transactions():
#     """Loads transactions from the file."""
#     try:
#         with open(TRANSACTIONS_FILE, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# # --- Core Features ---
# def set_budget():
#     """Sets a monthly budget for a category."""
#     category = questionary.select(
#         "Select category for budget:",
#         choices=EXPENSE_CATEGORIES
#     ).ask()

#     amount_str = questionary.text(
#         "Enter monthly budget amount for this category:",
#         validate=lambda text: text.replace('.', '', 1).isdigit() or "Please enter a valid number."
#     ).ask()
#     amount = int(float(amount_str) * 100) # Store as cents/paisa

#     budgets = load_budgets()
    
#     # Check if budget for this category already exists for the current month
#     current_month = datetime.now().strftime("%Y-%m")
#     found = False
#     for budget in budgets:
#         if budget["category"] == category and budget["month"] == current_month:
#             budget["amount"] = amount
#             found = True
#             break
    
#     if not found:
#         budgets.append({
#             "month": current_month,
#             "category": category,
#             "amount": amount
#         })
    
#     save_budgets(budgets)
#     console.print(f"[bold green]Budget for {category} set to Rs {amount/100:.2f} for {current_month}![/bold green]")

# def view_budgets():
#     """Displays current month's budgets and spending against them."""
#     budgets = load_budgets()
#     transactions = load_transactions()
#     current_month = datetime.now().strftime("%Y-%m")

#     # Filter budgets for the current month
#     monthly_budgets = [b for b in budgets if b["month"] == current_month]

#     if not monthly_budgets:
#         console.print("[bold yellow]No budgets set for the current month.[/bold yellow]")
#         return

#     # Calculate spending for the current month
#     spending_by_category = {}
#     for t in transactions:
#         transaction_date_month = datetime.strptime(t["date"], "%Y-%m-%d").strftime("%Y-%m")
#         if t["type"] == "Expense" and transaction_date_month == current_month:
#             spending_by_category[t["category"]] = spending_by_category.get(t["category"], 0) + t["amount"]

#     table = Table(title=f"Monthly Budgets for {current_month}")
#     table.add_column("Category", style="cyan")
#     table.add_column("Budget", justify="right", style="green")
#     table.add_column("Spent", justify="right", style="red")
#     table.add_column("Remaining", justify="right")
#     table.add_column("Utilization", justify="right")
#     table.add_column("Status", justify="center")

#     total_budget = 0
#     total_spent = 0
#     over_budget_categories = []

#     with Progress(
#         TextColumn("[progress.description]{task.description}"),
#         BarColumn(),
#         TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
#         ConsoleColumn(),
#         transient=True
#     ) as progress:
#         for budget in monthly_budgets:
#             category = budget["category"]
#             budget_amount = budget["amount"]
#             spent_amount = spending_by_category.get(category, 0)
#             remaining_amount = budget_amount - spent_amount
            
#             total_budget += budget_amount
#             total_spent += spent_amount

#             utilization_percent = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0

#             status_text = ""
#             status_style = ""
#             if utilization_percent >= 100:
#                 status_text = "OVER"
#                 status_style = "bold red"
#                 over_budget_categories.append(category)
#             elif utilization_percent >= 70:
#                 status_text = "WARNING"
#                 status_style = "bold yellow"
#             else:
#                 status_text = "OK"
#                 status_style = "bold green"

#             budget_display = f"Rs {budget_amount / 100:.2f}"
#             spent_display = f"Rs {spent_amount / 100:.2f}"
#             remaining_display = f"Rs {remaining_amount / 100:.2f}"
#             utilization_display = f"{utilization_percent:.2f}%"

#             task = progress.add_task(f"[white]{category}[/white]", total=100)
#             progress.update(task, completed=utilization_percent)

#             table.add_row(
#                 category,
#                 budget_display,
#                 spent_display,
#                 remaining_display,
#                 utilization_display,
#                 f"[{status_style}]{status_text}[/{status_style}]"
#             )
#     console.print(table)

#     # Overall Summary
#     console.print(f"\n[bold underline]Overall Monthly Budget Summary ({current_month}):[/bold underline]")
#     console.print(f"  [bold green]Total Budget:[/bold green] Rs {total_budget / 100:.2f}")
#     console.print(f"  [bold red]Total Spent:[/bold red]   Rs {total_spent / 100:.2f}")
#     overall_remaining = total_budget - total_spent
#     overall_remaining_style = "green" if overall_remaining >= 0 else "red"
#     console.print(f"  [bold {overall_remaining_style}]Total Remaining:[/bold {overall_remaining_style}] Rs {overall_remaining / 100:.2f}")
    
#     overall_utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
#     console.print(f"  [bold white]Overall Utilization:[/bold white] {overall_utilization:.2f}%")

#     if over_budget_categories:
#         console.print(f"  [bold red]Categories Over Budget:[/bold red] {', '.join(over_budget_categories)}")
#         console.print("[bold yellow]  Recommendation:[/bold yellow] Review spending in highlighted categories.")
#     else:
#         console.print("[bold green]  Good job! No categories are over budget.[/bold green]")


# def main():
#     """Main menu for budget management."""
#     while True:
#         choice = questionary.select(
#             "Budget Management",
#             choices=["Set Budget", "View Budgets", "Go Back"]
#         ).ask()

#         if choice == "Set Budget":
#             set_budget()
#         elif choice == "View Budgets":
#             view_budgets()
#         elif choice == "Go Back":
#             break

# if __name__ == "__main__":
#     main()



# features/budgets/budgets.py

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from datetime import datetime
import os

console = Console()

BUDGET_FILE = "database/budgets.txt"
TRANSACTION_FILE = "database/transactions.txt"

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health"]

# --- Load and Save Budgets ---
def load_budgets():
    budgets = {}
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            for line in f:
                if "," in line:
                    category, amount = line.strip().split(",")
                    budgets[category] = int(amount)
    return budgets

def save_budget(category, amount):
    budgets = load_budgets()
    budgets[category] = amount
    with open(BUDGET_FILE, "w") as f:
        for cat, amt in budgets.items():
            f.write(f"{cat},{amt}\n")

# --- Get total spent in a category ---
def get_spent(category):
    spent = 0
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as f:
            try:
                data = eval(f.read())  # read transactions as list of dicts
                for tx in data:
                    if tx.get("type") == "Expense" and tx.get("category") == category:
                        spent += int(tx.get("amount", 0))
            except:
                pass
    return spent

# --- Display budgets table ---
def show_budgets():
    console.print("\n[bold underline]Monthly Budget Overview[/bold underline]\n")
    budgets = load_budgets()
    table = Table(title="Budgets & Spending")
    table.add_column("Category", justify="left")
    table.add_column("Budget (Rs)", justify="right")
    table.add_column("Spent (Rs)", justify="right")
    table.add_column("Remaining (Rs)", justify="right")
    table.add_column("Usage", justify="left")

    with Progress(
        TextColumn("{task.fields[category]}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%")
    ) as progress:
        for category in CATEGORIES:
            budget = budgets.get(category, 0)
            spent = get_spent(category)
            remaining = budget - spent
            usage_percent = (spent / budget * 100) if budget > 0 else 0

            # Add to progress bar
            progress.add_task("", total=budget, completed=spent, category=category)

            table.add_row(
                category,
                f"{budget/100:.2f}",
                f"{spent/100:.2f}",
                f"{remaining/100:.2f}",
                f"{usage_percent:.0f}%"
            )

    console.print(table)

# --- Main budget management menu ---
def main():
    while True:
        console.print("\n[bold]Budget Management[/bold]")
        console.print("1. Set Budget")
        console.print("2. View Budgets")
        console.print("3. Back to Main Menu")
        choice = console.input("Enter choice: ").strip()

        if choice == "1":
            console.print("\nSet Budget for Categories")
            for idx, cat in enumerate(CATEGORIES, start=1):
                console.print(f"{idx}. {cat}")

            cat_choice_str = console.input("Select category (enter number): ").strip()
            try:
                cat_choice = int(cat_choice_str) - 1
                if cat_choice < 0 or cat_choice >= len(CATEGORIES):
                    console.print("[bold red]Invalid number! Try again.[/bold red]")
                    continue
                category = CATEGORIES[cat_choice]
            except ValueError:
                console.print("[bold red]Please enter a valid number![/bold red]")
                continue

            amount_str = console.input(f"Enter monthly budget for {category} (Rs): ").strip()
            try:
                amount = int(float(amount_str) * 100)  # Rs to paisa
            except ValueError:
                console.print("[bold red]Please enter a valid amount![/bold red]")
                continue

            save_budget(category, amount)
            console.print(f"[bold green]Budget for {category} set to Rs {amount/100:.2f} for this month![/bold green]")

        elif choice == "2":
            show_budgets()
        elif choice == "3":
            break
        else:
            console.print("[bold red]Invalid choice![/bold red]")

if __name__ == "__main__":
    main()
