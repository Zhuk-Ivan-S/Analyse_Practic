import pandas as pd
import io
import  matplotlib.pyplot as plt

'''# Створюємо імітацію CSV файлу
csv_data = """id,date,amount,category
1,2026-04-01,150.0,Retail
2,2026-04-02,-500.0,ATM
3,2026-04-02,,Online
4,2026-04-03,2000.0,Transfer
"""
df = pd.read_csv(io.StringIO(csv_data))

# ТВОЯ ЧЕРГА:
# 1. Виведи загальну інформацію про структуру (info)
print(df.info())

# 2. Виведи статистику (describe)
print(df.describe())
# 3. Знайди, у якій колонці є порожнє значення (NaN)
print(df.isnull().value_counts())
# 4 . average for empty
average_amount  = df['amount'].mean()
print(average_amount)
df['amount'] = df['amount'].fillna(0)
df['amount'] = df['amount'].replace(0,average_amount)
print(df['amount'])

# check for absolute and change
df['amount'] = df['amount'].abs()

# Save file
df.to_csv('../Practice/training.csv')

category_dt = df.groupby('category')['amount'].sum()

category_dt.plot(kind = 'bar', color = 'red')
plt.show()'''


'''def process_bank_data(file_path):
    df_work = pd.read_csv(file_path)

    df_work['amount'] = df_work['amount'].abs()
    df_work['amount'] = df_work['amount'].fillna(df_work['amount'].mean())
    report = df_work.groupby('category')['amount'].sum()
    return  report

print(process_bank_data('../Practice/training.csv'))
'''

import sqlite3
import pandas as pd


def consolidate_branches(db_path, excel_path):
    # 1. SQL Part
    conn = sqlite3.connect(db_path)
    df_a = pd.read_sql_query("SELECT * FROM branch_a", conn)

    # 2. Excel Part
    df_b = pd.read_excel(excel_path)

    # 3. Твоя черга: Об'єднай df_a та df_b за допомогою pd.concat
    df_full = pd.concat(df_a, df_b)
    # 4. Поверни суму колонки 'amount'
    reop = df_full['amount'].sum\()

    return  reop# твій результат

# Виклик:
# total = consolidate_branches('bank.db', 'branch_b.xlsx')