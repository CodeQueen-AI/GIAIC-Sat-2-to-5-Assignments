
import json
from datetime import datetime, timedelta
from collections import defaultdict
from rich.console import Console
from rich.panel import Panel

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

def get_monthly_transactions(transactions, year_month):
    """Filters transactions for a specific YYYY-MM."""
    return [t for t in transactions if t['date'].startswith(year_month)]

def get_expenses_by_category(transactions):
    """Aggregates expenses by category."""
    expenses = defaultdict(int)
    for t in transactions:
        if t['type'] == 'Expense':
            expenses[t['category']] += t['amount']
    return expenses

def analyze_high_spending(today):
    """Analyzes for unusually high spending categories."""
    transactions = load_data(TRANSACTIONS_FILE)
    budgets = load_data(BUDGETS_FILE)
    
    current_month_str = today.strftime("%Y-%m")
    last_month_str = (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    current_month_trans = get_monthly_transactions(transactions, current_month_str)
    last_month_trans = get_monthly_transactions(transactions, last_month_str)

    current_expenses = get_expenses_by_category(current_month_trans)
    last_expenses = get_expenses_by_category(last_month_trans)
    
    recommendations = []

    # 1. Compare with last month's spending
    for category, amount in current_expenses.items():
        last_month_amount = last_expenses.get(category, 0)
        if last_month_amount > 0 and amount > last_month_amount * 1.5: # 50% increase
             recommendations.append(
                f"Your spending on [bold yellow]'{category}'[/bold yellow] (Rs {amount/100:.2f}) is significantly higher than last month (Rs {last_month_amount/100:.2f}). Consider reviewing these expenses."
            )

    # 2. Compare with budget
    monthly_budgets = {b['category']: b['amount'] for b in budgets if b['month'] == current_month_str}
    for category, amount in current_expenses.items():
        budget_amount = monthly_budgets.get(category)
        if budget_amount and amount > budget_amount:
            recommendations.append(
                f"You are over budget on [bold red]'{category}'[/bold red]. You've spent Rs {amount/100:.2f}, which is over your budget of Rs {budget_amount/100:.2f}."
            )
            
    return recommendations

def find_recurring_payments(today):
    """Finds potential recurring payments/subscriptions."""
    transactions = load_data(TRANSACTIONS_FILE)
    # Look at transactions from the last 90 days for patterns
    ninety_days_ago = (today - timedelta(days=90)).strftime("%Y-%m-%d")
    recent_transactions = [t for t in transactions if t['date'] >= ninety_days_ago and t['type'] == 'Expense']

    potential_recurring = defaultdict(list)
    for t in recent_transactions:
        # Simple keyword matching for common subscription services
        keywords = ['netflix', 'spotify', 'subscription', 'prime', 'monthly', 'icloud']
        if any(keyword in t['description'].lower() for keyword in keywords):
            potential_recurring[t['description']].append(t['amount'])
    
    recommendations = []
    for desc, amounts in potential_recurring.items():
        if len(amounts) > 1: # If it appears more than once, it's likely recurring
            avg_amount = sum(amounts) / len(amounts)
            recommendations.append(
                f"We noticed a potential recurring payment for [bold cyan]'{desc}'[/bold cyan] with an average cost of Rs {avg_amount/100:.2f}. Is this subscription still necessary?"
            )
            
    return recommendations

def suggest_savings_opportunities():
    """Provides generic savings suggestions based on top spending categories."""
    transactions = load_data(TRANSACTIONS_FILE)
    today = datetime.now()
    current_month_trans = get_monthly_transactions(transactions, today.strftime("%Y-%m"))
    
    if not current_month_trans:
        return []

    expenses = get_expenses_by_category(current_month_trans)
    if not expenses:
        return []

    top_category = max(expenses, key=expenses.get)
    
    suggestions = {
        "Food": "Your top expense is 'Food'. You could potentially save money by planning meals and cooking at home more often.",
        "Shopping": "Your top expense is 'Shopping'. Consider creating a shopping list and sticking to it to avoid impulse buys.",
        "Transport": "Your top expense is 'Transport'. Look into carpooling or using public transport to save on fuel and maintenance costs.",
        "Entertainment": "Your top expense is 'Entertainment'. There are many free or low-cost entertainment options available, like visiting parks or libraries."
    }
    
    if top_category in suggestions:
        return [suggestions[top_category]]
    return []


def main():
    """Main function to display smart assistant recommendations."""
    console.print(Panel("[bold magenta]🚀 Smart Financial Assistant 🚀[/bold magenta]", expand=False))
    
    today = datetime.now()
    
    all_recommendations = []
    all_recommendations.extend(analyze_high_spending(today))
    all_recommendations.extend(find_recurring_payments(today))
    all_recommendations.extend(suggest_savings_opportunities())

    if not all_recommendations:
        console.print("[bold green]✅ Your finances are looking good! No immediate recommendations.[/bold green]")
        return

    console.print("[bold]Here are some personalized recommendations for you:[/bold]\n")
    for i, rec in enumerate(all_recommendations, 1):
        console.print(f"[cyan]{i}.[/cyan] {rec}\n")

if __name__ == "__main__":
    main()
