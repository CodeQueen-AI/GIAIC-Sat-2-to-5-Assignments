
import questionary
from features.transactions.transactions import main as transactions_main
from features.budgets.budgets import main as budgets_main
from features.analytics.analytics import main as analytics_main
from features.smart_assistant.smart_assistant import main as smart_assistant_main
from features.data_management.data_management import main as data_management_main

def main():
    while True:
        choice = questionary.select(
            "Welcome to the Personal Finance Tracker CLI!",
            choices=["Transaction Management", "Budget Management", "Financial Analytics", "Smart Assistant", "Data Management", "Web Dashboard", "Exit"]
        ).ask()

        if choice == "Transaction Management":
            transactions_main()
        elif choice == "Budget Management":
            budgets_main()
        elif choice == "Financial Analytics":
            analytics_main()
        elif choice == "Smart Assistant":
            smart_assistant_main()
        elif choice == "Data Management":
            data_management_main()
        elif choice == "Web Dashboard":
            web_dashboard_main()
        elif choice == "Exit":
            break

if __name__ == "__main__":
    main()
