import pandas as pd
import matplotlib.pyplot as plt
import  sqlite3

conn = sqlite3.connect('financial_data_training.db')
df = pd.read_sql_query('Select * FROM Cost_Transactions;', conn)
print(df.head(10))
print(df.dtypes)
print(df.isnull().sum())

# Month
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
print(df['Month'])

# top expenses per Month

top_expenses = df.groupby('Month')['Amount'].sum().sort_values(ascending = False)
print(top_expenses.head(10))

plt.figure(figsize= (8,6))
top_expenses.plot(kind = 'bar')
plt.xlabel('Month')
plt.ylabel('Amount')
plt.title('Expenses per month ')
plt.show()

# Top 5 CostCenters with most sum of expense

Top_CostCenters = df.groupby('CostCenter')['Amount'].sum().sort_values(ascending= False)
print(Top_CostCenters.head(5))

# show all cost centers in pie chart by expense
Top_CostCenters.plot(kind='pie', autopct = '%1.1f%%')
plt.show()

# Expense Type in Total expense

exp_type_sum = df.groupby('ExpenseType')['Amount'].sum()
print(exp_type_sum)
total_expense = df['Amount'].sum()
print(total_expense)
percent_in_total_expense = (exp_type_sum / total_expense) * 100
print(percent_in_total_expense)

# visual for expense type

plt.figure(figsize=(8,6))
exp_type_sum.plot(kind = 'pie', autopct = '%1.1f%%')
plt.show()
top_exp_month= df.groupby('Month')['Amount'].sum()
top_exp_month.plot(kind = 'line')
plt.show()

