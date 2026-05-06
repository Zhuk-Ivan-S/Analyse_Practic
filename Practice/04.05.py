import sqlite3
import  pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

bank_info = pd.read_csv('../Practice/german_credit_data.csv')

conn = sqlite3.connect('../Practice/bank.db')

bank_info.to_sql('credits',conn, index = False, if_exists='replace')

query = '''SELECT * FROM credits'''
df = pd.read_sql_query(query, conn)
print(df.info)
print(df.columns)
print(f'Duplicates in dataset : {df.duplicated().value_counts()}')
print(df.isnull().sum())
print(df['Saving accounts'].unique())
print(df['Checking account'].unique())

# Missing values in saving and checking

df_savings = df.groupby('Saving accounts')['Credit amount'].mean()
print(df_savings)

# Proto raiting with SQL
query = '''SELECT * , CASE WHEN Housing = "own" AND "Saving accounts" IN ("rich","quite rich") THEN "A" 
        WHEN Housing = "own" AND "Saving accounts" IN ("moderate") then "B" ELSE "C" END AS Credit_Rating FROM credits 
        WHERE "Credit amount" > 5000;'''
df_new = pd.read_sql_query(query,conn)
print(df_new.head(10))

# Default posibility
perfect_clients = df[
    (df['Housing'] == 'own') &
    (df['Purpose'] == 'car') &
    (df['Age'] >= 30) & (df['Age'] <= 40)
]

# Виводимо перші 5 рядків
print(perfect_clients.head(5))

