# Day 6: Data Management & Export

## Today's Goal
Implement utilities for managing financial data, including export and import functionalities.

## Learning Focus
- File I/O for different formats (CSV, JSON)
- Data serialization/deserialization
- Error handling for file operations

## Fintech Concepts
- **Data Portability**: Ability to move data between systems.
- **Backup & Restore**: Protecting data from loss.
- **Data Integrity**: Ensuring data is accurate and consistent.

## Features to Build

### 1. Export Data
- Allow users to export all transaction and budget data.
- Options: CSV, JSON.
- Prompt for filename and location.

### 2. Import Data (Future Goal)
- Allow users to import data from a CSV or JSON file.
- Implement robust validation to prevent data corruption.

### 3. Clear All Data (Admin Function)
- A risky operation, requiring strong confirmation.
- Clears both `transactions.txt` and `budgets.txt`.

## Success Criteria
✅ Can export data to CSV.
✅ Can export data to JSON.
✅ Handles file naming and location.
✅ Implements a secure "clear all data" function.
