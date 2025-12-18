import sqlite3
import random
from datetime import datetime, timedelta

cost_centers = ['Marketing','IT-Support','Production','R&D','Administration','Sales']
expense_types = ['Salary','Software_License','Travel','Utilities','Raw_Materials','Advertising']
statuses = ['Posted'] * 95 + ['Planned'] * 5
currency = 'EUR'

start_date = datetime(2025, 6, 1)
num_transactions = 100
def generate_transaction():
    random_days = random.randint(0,(datetime.now() - start_date).days)
    date = start_date + timedelta(days=random_days)
    cc = random.choice(expense_types)
    exp_type = random.choice(expense_types)
    amount = 0

    if exp_type == 'Salary':
        amount = random.randint(5000,15000)
    elif exp_type == 'Software_License':
        if cc == 'IT_Support':
            amount = random.randint(1000, 8000)
        else: amount = random.randint(100, 1000)
    elif exp_type == 'Advertising':
        if cc == 'Marketing':
            amount = random.randint(2000, 10000)
        else: amount = random.randint(50, 500)
    else: amount = random.randint(100, 3000)

    status = random.choice(statuses)
    return (
        date.strftime('%Y-%m-%d'),cc,exp_type,amount, currency,status)

try :
    conn = sqlite3.connect('financial_data_training.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cost_Transactions (TransactionID Integer primary key AUTOINCREMENT,
        Date Text NOT NULL,
        CostCenter Text NOT NULL,
        ExpenseType TEXT Not Null,
        Amount Real NOT NULL,
        Currency TEXT NOT NULL,
        Status TEXT NOT NULL)""")
    print('Table ceated')

    transactions = [generate_transaction() for _ in range (num_transactions)]
    cursor.executemany("""INSERT INTO Cost_Transactions (Date, CostCenter, ExpenseType, Amount, Currency, Status)
        VALUES (?,?,?,?,?,?)""",transactions)

    conn.commit()
    print(f'Successful added {num_transactions} ')

except sqlite3.Error as e:
    print(f'Error {e}')

finally:
    if conn:
        conn.close()

print('\nScript completed successful')

