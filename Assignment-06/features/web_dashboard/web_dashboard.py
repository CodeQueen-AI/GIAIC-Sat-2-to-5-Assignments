
# import streamlit as st
# import pandas as pd
# import json
# from datetime import datetime
# import plotly.express as px

# TRANSACTIONS_FILE = "database/transactions.txt"
# BUDGETS_FILE = "database/budgets.txt"

# def load_data(file_path):
#     """Loads JSON data from a file."""
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def main():
#     st.set_page_config(layout="wide")
#     st.title("💰 Personal Finance Dashboard")

#     transactions = load_data(TRANSACTIONS_FILE)
#     budgets = load_data(BUDGETS_FILE)

#     if not transactions:
#         st.warning("No transactions found. Add some transactions in the CLI to see data here!")
#         return

#     # Convert to DataFrame for easier manipulation
#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100 # Convert from paisa/cents to currency
#     df['date'] = pd.to_datetime(df['date'])

#     # Sidebar Filters
#     st.sidebar.header("Filters")
#     selected_month = st.sidebar.selectbox(
#         "Select Month",
#         options=df['date'].dt.strftime('%Y-%m').unique()
#     )

#     filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

#     # --- Overview Metrics ---
#     st.header("Overview")
#     total_income = filtered_df[filtered_df['type'] == 'Income']['amount'].sum()
#     total_expenses = filtered_df[filtered_df['type'] == 'Expense']['amount'].sum()
#     balance = total_income - total_expenses

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Income", f"Rs {total_income:.2f}", delta_color="inverse")
#     with col2:
#         st.metric("Total Expenses", f"Rs {total_expenses:.2f}", delta_color="off")
#     with col3:
#         st.metric("Current Balance", f"Rs {balance:.2f}", delta_color="off")

#     st.markdown("--- ")

#     # --- Spending Breakdown by Category ---
#     st.header("Spending Breakdown")
#     expense_df = filtered_df[filtered_df['type'] == 'Expense']
#     spending_by_category = expense_df.groupby('category')['amount'].sum().reset_index()

#     if not spending_by_category.empty:
#         fig = px.pie(spending_by_category, values='amount', names='category',
#                      title=f'Spending by Category for {selected_month}')
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No expenses for selected month.")

#     st.markdown("--- ")

#     # --- Transactions Table ---
#     st.header("All Transactions")
#     st.dataframe(filtered_df.sort_values(by='date', ascending=False), use_container_width=True)

#     st.markdown("--- ")

#     # --- Budget vs. Actual (for selected month) ---
#     st.header("Budget vs. Actual")
#     if budgets:
#         budgets_df = pd.DataFrame(budgets)
#         budgets_df['amount'] = budgets_df['amount'] / 100 # Convert from paisa/cents
        
#         current_month_budgets = budgets_df[budgets_df['month'] == selected_month]
        
#         if not current_month_budgets.empty:
#             # Merge with actual spending
#             merged_df = pd.merge(current_month_budgets, spending_by_category,
#                                  on='category', how='left')
#             merged_df['amount_y'] = merged_df['amount_y'].fillna(0) # Fill NaNs for categories with no spending
#             merged_df.rename(columns={'amount_x': 'Budgeted', 'amount_y': 'Spent'}, inplace=True)

#             fig_budget = px.bar(merged_df, x='category', y=['Budgeted', 'Spent'],
#                                 title=f'Budget vs. Actual for {selected_month}',
#                                 barmode='group')
#             st.plotly_chart(fig_budget, use_container_width=True)
#         else:
#             st.info("No budgets set for the selected month.")
#     else:
#         st.info("No budgets set.")


# if __name__ == "__main__":
#     main()

# import streamlit as st
# import pandas as pd
# import json
# import plotly.express as px
# from datetime import datetime

# # File paths
# TRANSACTIONS_FILE = "database/transactions.txt"
# BUDGETS_FILE = "database/budgets.txt"

# # Utility function to load JSON data
# def load_data(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# # --- Transaction Dashboard ---
# def show_transactions_dashboard():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found. Add some transactions in the CLI to see data here!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("💳 Transaction Management")
#     st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)

# # --- Budget Dashboard ---
# def show_budget_dashboard():
#     budgets_raw = []
#     with open(BUDGETS_FILE, 'r') as f:
#         for line in f:
#             if "," in line:
#                 category, amount = line.strip().split(",")
#                 budgets_raw.append({"category": category, "amount": int(amount)})

#     if not budgets_raw:
#         st.info("No budgets found. Set budgets in the CLI to see them here!")
#         return

#     budgets_df = pd.DataFrame(budgets_raw)
#     budgets_df['amount'] = budgets_df['amount'] / 100
#     st.header("📊 Budget Management")
#     st.dataframe(budgets_df, use_container_width=True)

# # --- Financial Analytics (example) ---
# def show_financial_analytics():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found to analyze!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("📈 Financial Analytics")
#     income_df = df[df['type'] == "Income"].groupby("category")['amount'].sum().reset_index()
#     expense_df = df[df['type'] == "Expense"].groupby("category")['amount'].sum().reset_index()

#     st.subheader("Income by Category")
#     if not income_df.empty:
#         fig_income = px.pie(income_df, values='amount', names='category')
#         st.plotly_chart(fig_income, use_container_width=True)
#     else:
#         st.info("No income data available.")

#     st.subheader("Expenses by Category")
#     if not expense_df.empty:
#         fig_expense = px.bar(expense_df, x='category', y='amount', title="Expenses by Category")
#         st.plotly_chart(fig_expense, use_container_width=True)
#     else:
#         st.info("No expense data available.")

# # --- Smart Assistant placeholder ---
# def show_smart_assistant():
#     st.header("🤖 Smart Assistant")
#     st.info("This section will include AI-powered suggestions and tools in the future.")

# # --- Data Management placeholder ---
# def show_data_management():
#     st.header("🗄️ Data Management")
#     st.info("This section will allow you to import/export transactions and budgets in the future.")

# # --- Web Dashboard placeholder ---
# def show_web_dashboard():
#     st.header("🌐 Web Dashboard")
#     st.info("This section will integrate web-based dashboards in the future.")

# # --- Main App ---
# def main():
#     st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
#     st.title("💰 Personal Finance Dashboard")

#     section = st.sidebar.selectbox(
#         "Select Section",
#         [
#             "Transaction Management",
#             "Budget Management",
#             "Financial Analytics",
#             "Smart Assistant",
#             "Data Management",
#             "Web Dashboard"
#         ]
#     )

#     if section == "Transaction Management":
#         show_transactions_dashboard()
#     elif section == "Budget Management":
#         show_budget_dashboard()
#     elif section == "Financial Analytics":
#         show_financial_analytics()
#     elif section == "Smart Assistant":
#         show_smart_assistant()
#     elif section == "Data Management":
#         show_data_management()
#     elif section == "Web Dashboard":
#         show_web_dashboard()

# if __name__ == "__main__":
#     main()












# import streamlit as st
# import pandas as pd
# import json
# from datetime import datetime
# import plotly.express as px

# TRANSACTIONS_FILE = "database/transactions.txt"
# BUDGETS_FILE = "database/budgets.txt"

# def load_data(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# # --- Transaction Dashboard ---
# def show_transactions_dashboard():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found. Add some transactions in the CLI to see data here!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("💳 Transaction Management")
    
#     # Sidebar filter by month
#     months = df['date'].dt.strftime('%Y-%m').unique()
#     selected_month = st.sidebar.selectbox("Filter Month (Transactions)", months)
#     filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

#     # Overview Metrics
#     total_income = filtered_df[filtered_df['type'] == "Income"]['amount'].sum()
#     total_expenses = filtered_df[filtered_df['type'] == "Expense"]['amount'].sum()
#     balance = total_income - total_expenses

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Income", f"Rs {total_income:.2f}")
#     col2.metric("Total Expenses", f"Rs {total_expenses:.2f}")
#     col3.metric("Current Balance", f"Rs {balance:.2f}")

#     st.markdown("---")
    
#     # Spending by Category Pie Chart
#     expense_df = filtered_df[filtered_df['type'] == "Expense"]
#     if not expense_df.empty:
#         spending_by_category = expense_df.groupby("category")['amount'].sum().reset_index()
#         fig = px.pie(spending_by_category, values='amount', names='category',
#                      title=f'Spending by Category ({selected_month})')
#         st.plotly_chart(fig, use_container_width=True)
    
#     # Transactions Table
#     st.subheader("All Transactions")
#     st.dataframe(filtered_df.sort_values(by='date', ascending=False), use_container_width=True)

# # --- Budget Dashboard ---
# def show_budget_dashboard():
#     budgets_raw = []
#     with open(BUDGETS_FILE, 'r') as f:
#         for line in f:
#             if "," in line:
#                 category, amount = line.strip().split(",")
#                 budgets_raw.append({"category": category, "amount": int(amount)})

#     if not budgets_raw:
#         st.info("No budgets found. Set budgets in the CLI to see them here!")
#         return

#     budgets_df = pd.DataFrame(budgets_raw)
#     budgets_df['amount'] = budgets_df['amount'] / 100

#     # Sidebar filter by month (if your budgets file has month info, can be used)
#     st.header("📊 Budget Management")
    
#     # Merge with actual spent
#     transactions = load_data(TRANSACTIONS_FILE)
#     if transactions:
#         trans_df = pd.DataFrame(transactions)
#         trans_df['amount'] = trans_df['amount'] / 100
#         spent_by_category = trans_df.groupby("category")['amount'].sum().reset_index()
#         merged_df = pd.merge(budgets_df, spent_by_category, on="category", how="left").fillna(0)
#         merged_df.rename(columns={"amount_x": "Budgeted", "amount_y": "Spent"}, inplace=True)

#         # Show bar chart Budget vs Actual
#         fig_budget = px.bar(merged_df, x="category", y=["Budgeted", "Spent"],
#                             title="Budget vs Actual by Category", barmode="group")
#         st.plotly_chart(fig_budget, use_container_width=True)

#         # Show table
#         st.subheader("Budgets & Spending Table")
#         merged_df['Remaining'] = merged_df['Budgeted'] - merged_df['Spent']
#         st.dataframe(merged_df, use_container_width=True)
#     else:
#         st.dataframe(budgets_df, use_container_width=True)

# # --- Financial Analytics ---
# def show_financial_analytics():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found to analyze!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("📈 Financial Analytics")
#     income_df = df[df['type'] == "Income"].groupby("category")['amount'].sum().reset_index()
#     expense_df = df[df['type'] == "Expense"].groupby("category")['amount'].sum().reset_index()

#     if not income_df.empty:
#         fig_income = px.pie(income_df, values='amount', names='category', title="Income by Category")
#         st.plotly_chart(fig_income, use_container_width=True)
#     if not expense_df.empty:
#         fig_expense = px.bar(expense_df, x='category', y='amount', title="Expenses by Category")
#         st.plotly_chart(fig_expense, use_container_width=True)

# # --- Smart Assistant placeholder ---
# def show_smart_assistant():
#     st.header("🤖 Smart Assistant")
#     st.info("AI-powered suggestions will appear here.")

# # --- Data Management placeholder ---
# def show_data_management():
#     st.header("🗄️ Data Management")
#     st.info("Import/export transactions and budgets here.")

# # --- Web Dashboard placeholder ---
# def show_web_dashboard():
#     st.header("🌐 Web Dashboard")
#     st.info("Web dashboards will appear here.")

# # --- Main App ---
# def main():
#     st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
#     st.title("💰 Personal Finance Dashboard")

#     section = st.sidebar.selectbox(
#         "Select Section",
#         [
#             "Transaction Management",
#             "Budget Management",
#             "Financial Analytics",
#             "Smart Assistant",
#             "Data Management",
#             "Web Dashboard"
#         ]
#     )

#     if section == "Transaction Management":
#         show_transactions_dashboard()
#     elif section == "Budget Management":
#         show_budget_dashboard()
#     elif section == "Financial Analytics":
#         show_financial_analytics()
#     elif section == "Smart Assistant":
#         show_smart_assistant()
#     elif section == "Data Management":
#         show_data_management()
#     elif section == "Web Dashboard":
#         show_web_dashboard()

# if __name__ == "__main__":
#     main()







# import streamlit as st
# import pandas as pd
# import json
# from datetime import datetime
# import plotly.express as px

# TRANSACTIONS_FILE = "database/transactions.txt"
# BUDGETS_FILE = "database/budgets.txt"

# def load_data(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# # --- Smart Suggestions Engine ---
# def generate_suggestions(transactions, budgets, selected_month):
#     suggestions = []
    
#     if not transactions or not budgets:
#         return ["No data available for suggestions."]
    
#     budget_dict = {b['category']: b['amount']/100 for b in budgets if 'category' in b and 'amount' in b}
    
#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])
#     filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

#     if filtered_df.empty:
#         return ["No transactions for the selected month."]

#     expense_df = filtered_df[filtered_df['type'] == 'Expense']
#     spending_by_category = expense_df.groupby('category')['amount'].sum().to_dict()

#     for category, spent in spending_by_category.items():
#         budgeted = budget_dict.get(category, 0)
#         if budgeted == 0:
#             suggestions.append(f"Category '{category}' has expenses but no budget set.")
#         elif spent > budgeted:
#             suggestions.append(f"⚠ You have overspent in '{category}' by Rs {spent - budgeted:.2f}.")
#         elif spent > 0.8 * budgeted:
#             suggestions.append(f"🔔 You are close to the budget limit in '{category}'.")
#         else:
#             suggestions.append(f"✅ '{category}' spending is under control.")

#     total_income = filtered_df[filtered_df['type'] == 'Income']['amount'].sum()
#     total_expenses = expense_df['amount'].sum()
#     if total_income > 0 and total_expenses / total_income > 0.8:
#         suggestions.append("💡 Your expenses are high compared to income. Consider saving more.")

#     return suggestions if suggestions else ["No significant suggestions for this month."]

# # --- Transaction Dashboard ---
# def show_transactions_dashboard():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found. Add transactions in CLI first!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("💳 Transaction Management")
    
#     months = df['date'].dt.strftime('%Y-%m').unique()
#     selected_month = st.sidebar.selectbox("Filter Month (Transactions)", months)
#     filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

#     total_income = filtered_df[filtered_df['type'] == "Income"]['amount'].sum()
#     total_expenses = filtered_df[filtered_df['type'] == "Expense"]['amount'].sum()
#     balance = total_income - total_expenses

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Income", f"Rs {total_income:.2f}")
#     col2.metric("Total Expenses", f"Rs {total_expenses:.2f}")
#     col3.metric("Current Balance", f"Rs {balance:.2f}")

#     st.markdown("---")
    
#     expense_df = filtered_df[filtered_df['type'] == "Expense"]
#     if not expense_df.empty:
#         spending_by_category = expense_df.groupby("category")['amount'].sum().reset_index()
#         fig = px.pie(spending_by_category, values='amount', names='category',
#                      title=f'Spending by Category ({selected_month})')
#         st.plotly_chart(fig, use_container_width=True)
    
#     st.subheader("All Transactions")
#     st.dataframe(filtered_df.sort_values(by='date', ascending=False), use_container_width=True)

# # --- Budget Dashboard ---
# def show_budget_dashboard():
#     budgets_raw = []
#     with open(BUDGETS_FILE, 'r') as f:
#         for line in f:
#             if "," in line:
#                 category, amount = line.strip().split(",")
#                 budgets_raw.append({"category": category, "amount": int(amount)})

#     if not budgets_raw:
#         st.info("No budgets found. Set budgets in CLI first!")
#         return

#     budgets_df = pd.DataFrame(budgets_raw)
#     budgets_df['amount'] = budgets_df['amount'] / 100

#     st.header("📊 Budget Management")
    
#     transactions = load_data(TRANSACTIONS_FILE)
#     if transactions:
#         trans_df = pd.DataFrame(transactions)
#         trans_df['amount'] = trans_df['amount'] / 100
#         spent_by_category = trans_df.groupby("category")['amount'].sum().reset_index()
#         merged_df = pd.merge(budgets_df, spent_by_category, on="category", how="left").fillna(0)
#         merged_df.rename(columns={"amount_x": "Budgeted", "amount_y": "Spent"}, inplace=True)
#         merged_df['Remaining'] = merged_df['Budgeted'] - merged_df['Spent']

#         # Bar chart
#         fig_budget = px.bar(merged_df, x="category", y=["Budgeted", "Spent"],
#                             title="Budget vs Actual by Category", barmode="group")
#         st.plotly_chart(fig_budget, use_container_width=True)

#         st.subheader("Budgets & Spending Table")
#         st.dataframe(merged_df, use_container_width=True)
#     else:
#         st.dataframe(budgets_df, use_container_width=True)

# # --- Financial Analytics ---
# def show_financial_analytics():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions to analyze!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("📈 Financial Analytics")
#     income_df = df[df['type'] == "Income"].groupby("category")['amount'].sum().reset_index()
#     expense_df = df[df['type'] == "Expense"].groupby("category")['amount'].sum().reset_index()

#     if not income_df.empty:
#         fig_income = px.pie(income_df, values='amount', names='category', title="Income by Category")
#         st.plotly_chart(fig_income, use_container_width=True)
#     if not expense_df.empty:
#         fig_expense = px.bar(expense_df, x='category', y='amount', title="Expenses by Category")
#         st.plotly_chart(fig_expense, use_container_width=True)

# # --- Smart Assistant ---
# def show_smart_assistant():
#     st.header("🤖 Smart Assistant")
#     transactions = load_data(TRANSACTIONS_FILE)
#     budgets_raw = []
#     with open(BUDGETS_FILE, 'r') as f:
#         for line in f:
#             if "," in line:
#                 category, amount = line.strip().split(",")
#                 budgets_raw.append({"category": category, "amount": int(amount)})

#     months = pd.to_datetime([t['date'] for t in transactions]).strftime('%Y-%m').unique() if transactions else ["N/A"]
#     selected_month = st.selectbox("Select Month for Suggestions", months)

#     suggestions = generate_suggestions(transactions, budgets_raw, selected_month)

#     st.subheader("💡 Suggestions")
#     for s in suggestions:
#         st.info(s)

#     # Visual summary in Smart Assistant
#     if transactions:
#         df = pd.DataFrame(transactions)
#         df['amount'] = df['amount'] / 100
#         df['date'] = pd.to_datetime(df['date'])
#         filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

#         if not filtered_df.empty:
#             spent_by_category = filtered_df[filtered_df['type'] == 'Expense'].groupby('category')['amount'].sum().reset_index()
#             if not spent_by_category.empty:
#                 fig = px.bar(spent_by_category, x='category', y='amount', title=f'Expenses by Category ({selected_month})', text='amount')
#                 st.plotly_chart(fig, use_container_width=True)

# # --- Data Management ---
# def show_data_management():
#     st.header("🗄️ Data Management")
#     st.info("Import/export transactions and budgets here.")

# # --- Web Dashboard ---
# def show_web_dashboard():
#     st.header("🌐 Web Dashboard")
#     st.info("Web dashboards will appear here.")

# # --- Main App ---
# def main():
#     st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
#     st.title("💰 Personal Finance Dashboard")

#     section = st.sidebar.selectbox(
#         "Select Section",
#         [
#             "Transaction Management",
#             "Budget Management",
#             "Financial Analytics",
#             "Smart Assistant",
#             "Data Management",
#             "Web Dashboard"
#         ]
#     )

#     if section == "Transaction Management":
#         show_transactions_dashboard()
#     elif section == "Budget Management":
#         show_budget_dashboard()
#     elif section == "Financial Analytics":
#         show_financial_analytics()
#     elif section == "Smart Assistant":
#         show_smart_assistant()
#     elif section == "Data Management":
#         show_data_management()
#     elif section == "Web Dashboard":
#         show_web_dashboard()

# if __name__ == "__main__":
#     main()








# import streamlit as st
# import pandas as pd
# import json
# from datetime import datetime
# import plotly.express as px
# from io import StringIO

# TRANSACTIONS_FILE = "database/transactions.txt"
# BUDGETS_FILE = "database/budgets.txt"

# def load_data(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def save_transactions(transactions):
#     with open(TRANSACTIONS_FILE, 'w') as f:
#         json.dump(transactions, f, indent=4)

# # --- Transaction Dashboard ---
# def show_transactions_dashboard():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found. Add some transactions in the CLI to see data here!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("💳 Transaction Management")
    
#     # Sidebar filter by month
#     months = df['date'].dt.strftime('%Y-%m').unique()
#     selected_month = st.sidebar.selectbox("Filter Month (Transactions)", months)
#     filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

#     # Overview Metrics
#     total_income = filtered_df[filtered_df['type'] == "Income"]['amount'].sum()
#     total_expenses = filtered_df[filtered_df['type'] == "Expense"]['amount'].sum()
#     balance = total_income - total_expenses

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Income", f"Rs {total_income:.2f}")
#     col2.metric("Total Expenses", f"Rs {total_expenses:.2f}")
#     col3.metric("Current Balance", f"Rs {balance:.2f}")

#     st.markdown("---")
    
#     # Spending by Category Pie Chart
#     expense_df = filtered_df[filtered_df['type'] == "Expense"]
#     if not expense_df.empty:
#         spending_by_category = expense_df.groupby("category")['amount'].sum().reset_index()
#         fig = px.pie(spending_by_category, values='amount', names='category',
#                      title=f'Spending by Category ({selected_month})')
#         st.plotly_chart(fig, use_container_width=True)
    
#     # Transactions Table
#     st.subheader("All Transactions")
#     st.dataframe(filtered_df.sort_values(by='date', ascending=False), use_container_width=True)

# # --- Budget Dashboard ---
# def show_budget_dashboard():
#     budgets_raw = []
#     try:
#         with open(BUDGETS_FILE, 'r') as f:
#             for line in f:
#                 if "," in line:
#                     category, amount = line.strip().split(",")
#                     budgets_raw.append({"category": category, "amount": int(amount)})
#     except FileNotFoundError:
#         st.info("Budgets file not found. Set budgets in CLI first.")

#     if not budgets_raw:
#         st.info("No budgets found. Set budgets in the CLI to see them here!")
#         return

#     budgets_df = pd.DataFrame(budgets_raw)
#     budgets_df['amount'] = budgets_df['amount'] / 100

#     st.header("📊 Budget Management")
    
#     # Merge with actual spent
#     transactions = load_data(TRANSACTIONS_FILE)
#     if transactions:
#         trans_df = pd.DataFrame(transactions)
#         trans_df['amount'] = trans_df['amount'] / 100
#         spent_by_category = trans_df.groupby("category")['amount'].sum().reset_index()
#         merged_df = pd.merge(budgets_df, spent_by_category, on="category", how="left").fillna(0)
#         merged_df.rename(columns={"amount_x": "Budgeted", "amount_y": "Spent"}, inplace=True)

#         # Bar chart Budget vs Actual
#         fig_budget = px.bar(merged_df, x="category", y=["Budgeted", "Spent"],
#                             title="Budget vs Actual by Category", barmode="group")
#         st.plotly_chart(fig_budget, use_container_width=True)

#         # Table
#         merged_df['Remaining'] = merged_df['Budgeted'] - merged_df['Spent']
#         st.subheader("Budgets & Spending Table")
#         st.dataframe(merged_df, use_container_width=True)
#     else:
#         st.dataframe(budgets_df, use_container_width=True)

# # --- Financial Analytics ---
# def show_financial_analytics():
#     transactions = load_data(TRANSACTIONS_FILE)
#     if not transactions:
#         st.warning("No transactions found to analyze!")
#         return

#     df = pd.DataFrame(transactions)
#     df['amount'] = df['amount'] / 100
#     df['date'] = pd.to_datetime(df['date'])

#     st.header("📈 Financial Analytics")
#     income_df = df[df['type'] == "Income"].groupby("category")['amount'].sum().reset_index()
#     expense_df = df[df['type'] == "Expense"].groupby("category")['amount'].sum().reset_index()

#     if not income_df.empty:
#         fig_income = px.pie(income_df, values='amount', names='category', title="Income by Category")
#         st.plotly_chart(fig_income, use_container_width=True)
#     if not expense_df.empty:
#         fig_expense = px.bar(expense_df, x='category', y='amount', title="Expenses by Category")
#         st.plotly_chart(fig_expense, use_container_width=True)

# # --- Smart Assistant ---
# def show_smart_assistant():
#     st.header("🤖 Smart Assistant")
#     st.info("AI-powered suggestions and insights will appear here.")

# # --- Data Management ---
# def show_data_management():
#     st.header("🗄️ Data Management")
#     st.subheader("Export Data")
    
#     transactions = load_data(TRANSACTIONS_FILE)
#     budgets_raw = []
#     try:
#         with open(BUDGETS_FILE, 'r') as f:
#             for line in f:
#                 if "," in line:
#                     category, amount = line.strip().split(",")
#                     budgets_raw.append({"category": category, "amount": int(amount)})
#     except FileNotFoundError:
#         budgets_raw = []
    
#     budgets_df = pd.DataFrame(budgets_raw)

#     if transactions:
#         st.download_button(
#             label="Download Transactions as JSON",
#             data=json.dumps(transactions, indent=4),
#             file_name="transactions.json",
#             mime="application/json"
#         )
#     if not budgets_df.empty:
#         st.download_button(
#             label="Download Budgets as CSV",
#             data=budgets_df.to_csv(index=False),
#             file_name="budgets.csv",
#             mime="text/csv"
#         )
    
#     st.subheader("Import Data")
#     uploaded_trans = st.file_uploader("Upload Transactions JSON", type=["json"])
#     if uploaded_trans:
#         try:
#             loaded_trans = json.load(uploaded_trans)
#             save_transactions(loaded_trans)
#             st.success("Transactions imported successfully! Please refresh page.")
#         except Exception as e:
#             st.error(f"Error importing transactions: {e}")

# # --- Web Dashboard ---
# def show_web_dashboard():
#     st.header("🌐 Web Dashboard")
#     st.info("Web dashboards will appear here.")

# # --- Main App ---
# def main():
#     st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
#     st.title("💰 Personal Finance Dashboard")

#     section = st.sidebar.selectbox(
#         "Select Section",
#         [
#             "Transaction Management",
#             "Budget Management",
#             "Financial Analytics",
#             "Smart Assistant",
#             "Data Management",
#             "Web Dashboard"
#         ]
#     )

#     if section == "Transaction Management":
#         show_transactions_dashboard()
#     elif section == "Budget Management":
#         show_budget_dashboard()
#     elif section == "Financial Analytics":
#         show_financial_analytics()
#     elif section == "Smart Assistant":
#         show_smart_assistant()
#     elif section == "Data Management":
#         show_data_management()
#     elif section == "Web Dashboard":
#         show_web_dashboard()

# if __name__ == "__main__":
#     main()























































import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

TRANSACTIONS_FILE = "database/transactions.txt"
BUDGETS_FILE = "database/budgets.txt"

# --- Helper Functions ---
def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

def save_budgets(budgets):
    with open(BUDGETS_FILE, 'w') as f:
        f.writelines([f"{b['category']},{b['amount']}\n" for b in budgets])

# --- Transaction Dashboard ---
def show_transactions_dashboard():
    transactions = load_data(TRANSACTIONS_FILE)
    if not transactions:
        st.warning("No transactions found. Add some transactions in the CLI to see data here!")
        return

    df = pd.DataFrame(transactions)
    df['amount'] = df['amount'] / 100
    df['date'] = pd.to_datetime(df['date'])

    st.header("💳 Transaction Management")
    
    months = df['date'].dt.strftime('%Y-%m').unique()
    selected_month = st.sidebar.selectbox("Filter Month (Transactions)", months)
    filtered_df = df[df['date'].dt.strftime('%Y-%m') == selected_month]

    total_income = filtered_df[filtered_df['type'] == "Income"]['amount'].sum()
    total_expenses = filtered_df[filtered_df['type'] == "Expense"]['amount'].sum()
    balance = total_income - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rs {total_income:.2f}")
    col2.metric("Total Expenses", f"Rs {total_expenses:.2f}")
    col3.metric("Current Balance", f"Rs {balance:.2f}")

    st.markdown("---")
    
    # Spending by Category Pie Chart
    expense_df = filtered_df[filtered_df['type'] == "Expense"]
    if not expense_df.empty:
        spending_by_category = expense_df.groupby("category")['amount'].sum().reset_index()
        fig = px.pie(spending_by_category, values='amount', names='category',
                     title=f'Spending by Category ({selected_month})')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("All Transactions")
    st.dataframe(filtered_df.sort_values(by='date', ascending=False), use_container_width=True)

# --- Budget Dashboard ---
def show_budget_dashboard():
    budgets_raw = []
    if os.path.exists(BUDGETS_FILE):
        with open(BUDGETS_FILE, 'r') as f:
            for line in f:
                if "," in line:
                    category, amount = line.strip().split(",")
                    budgets_raw.append({"category": category, "amount": int(amount)})

    if not budgets_raw:
        st.info("No budgets found. Set budgets in the CLI to see them here!")
        return

    budgets_df = pd.DataFrame(budgets_raw)
    budgets_df['amount'] = budgets_df['amount'] / 100

    st.header("📊 Budget Management")

    transactions = load_data(TRANSACTIONS_FILE)
    if transactions:
        trans_df = pd.DataFrame(transactions)
        trans_df['amount'] = trans_df['amount'] / 100
        spent_by_category = trans_df.groupby("category")['amount'].sum().reset_index()
        merged_df = pd.merge(budgets_df, spent_by_category, on="category", how="left").fillna(0)
        merged_df.rename(columns={"amount_x": "Budgeted", "amount_y": "Spent"}, inplace=True)
        merged_df['Remaining'] = merged_df['Budgeted'] - merged_df['Spent']

        fig_budget = px.bar(merged_df, x="category", y=["Budgeted", "Spent"],
                            title="Budget vs Actual by Category", barmode="group")
        st.plotly_chart(fig_budget, use_container_width=True)

        st.subheader("Budgets & Spending Table")
        st.dataframe(merged_df, use_container_width=True)
    else:
        st.dataframe(budgets_df, use_container_width=True)

# --- Financial Analytics ---
def show_financial_analytics():
    transactions = load_data(TRANSACTIONS_FILE)
    if not transactions:
        st.warning("No transactions found to analyze!")
        return

    df = pd.DataFrame(transactions)
    df['amount'] = df['amount'] / 100
    df['date'] = pd.to_datetime(df['date'])

    st.header("📈 Financial Analytics")
    income_df = df[df['type'] == "Income"].groupby("category")['amount'].sum().reset_index()
    expense_df = df[df['type'] == "Expense"].groupby("category")['amount'].sum().reset_index()

    if not income_df.empty:
        fig_income = px.pie(income_df, values='amount', names='category', title="Income by Category")
        st.plotly_chart(fig_income, use_container_width=True)
    if not expense_df.empty:
        fig_expense = px.bar(expense_df, x='category', y='amount', title="Expenses by Category")
        st.plotly_chart(fig_expense, use_container_width=True)

# --- Smart Assistant ---
def show_smart_assistant():
    st.header("🤖 Smart Assistant")
    st.info("AI-powered suggestions will appear here.")

# --- Data Management ---
def show_data_management():
    st.header("🗄️ Data Management")
    st.info("Import/export transactions and budgets here.")

    # Upload Transactions CSV
    uploaded_transactions = st.file_uploader("Upload Transactions CSV", type=["csv"])
    if uploaded_transactions:
        df = pd.read_csv(uploaded_transactions)
        transactions = df.to_dict(orient="records")
        save_transactions(transactions)
        st.success("Transactions imported successfully!")

    # Upload Budgets CSV
    uploaded_budgets = st.file_uploader("Upload Budgets CSV", type=["csv"])
    if uploaded_budgets:
        df = pd.read_csv(uploaded_budgets)
        budgets = [{"category": row['category'], "amount": int(row['amount'])} for idx, row in df.iterrows()]
        save_budgets(budgets)
        st.success("Budgets imported successfully!")

    if st.button("Export Transactions CSV"):
        transactions = load_data(TRANSACTIONS_FILE)
        pd.DataFrame(transactions).to_csv("transactions_export.csv", index=False)
        st.success("Transactions exported as transactions_export.csv")

    # Export Budgets
    if st.button("Export Budgets CSV"):
        budgets_raw = []
        if os.path.exists(BUDGETS_FILE):
            with open(BUDGETS_FILE, 'r') as f:
                for line in f:
                    if "," in line:
                        category, amount = line.strip().split(",")
                        budgets_raw.append({"category": category, "amount": int(amount)})
        pd.DataFrame(budgets_raw).to_csv("budgets_export.csv", index=False)
        st.success("Budgets exported as budgets_export.csv")

# --- Web Dashboard ---
def show_web_dashboard():
    st.header("🌐 Web Dashboard")
    st.info("Overview of all financial metrics and graphs here.")

    show_transactions_dashboard()
    st.markdown("---")
    show_budget_dashboard()
    st.markdown("---")
    show_financial_analytics()

# --- Main App ---
def main():
    st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
    st.title("💰 Personal Finance Dashboard")

    section = st.sidebar.selectbox(
        "Select Section",
        [
            "Transaction Management",
            "Budget Management",
            "Financial Analytics",
            "Smart Assistant",
            "Data Management",
            "Web Dashboard"
        ]
    )

    if section == "Transaction Management":
        show_transactions_dashboard()
    elif section == "Budget Management":
        show_budget_dashboard()
    elif section == "Financial Analytics":
        show_financial_analytics()
    elif section == "Smart Assistant":
        show_smart_assistant()
    elif section == "Data Management":
        show_data_management()
    elif section == "Web Dashboard":
        show_web_dashboard()

if __name__ == "__main__":
    main()
