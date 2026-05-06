import pandas as pd

# Дані про ліміти
#customers_data = {
   # 'customer_id': [101, 102, 103, 104],
    #'credit_limit': [5000, 2000, 10000, 3000]
#}
#df_customers = pd.DataFrame(customers_data)

# Дані про витрати
#spending_data = {
 #   'customer_id': [101, 101, 102, 104, 104, 104],
  #  'spent_amount': [2000, 3500, 1500, 1000, 1500, 1200]
#}
#df_spending = pd.DataFrame(spending_data)

#client_group = df_spending.groupby('customer_id')['spent_amount'].sum()
#print(client_group) # групування і відображення по кожному клієнту

#df_full = pd.merge(df_customers, client_group, on = 'customer_id', how = 'left') # обєднання таблиць в загальну

#df_full = df_full.dropna() # очишення Nan

#df_full['Over_Limit'] = df_full['spent_amount'] - df_full['credit_limit']

#print(f"List of clients : {df_full[df_full['Over_Limit']>0]}")
#____________________________________________________________________________________


data = {
    'bill_date': pd.to_datetime(['2026-01-01', '2026-01-05', '2026-01-10']),
    'pay_date': pd.to_datetime(['2026-01-05', '2026-01-20', '2026-01-11'])
}
df_bills = pd.DataFrame(data)
print(df_bills)

df_bills['days_to_pay'] = (df_bills['pay_date'] - df_bills['bill_date']).dt.days
print(df_bills['days_to_pay'])
print(f'Average days for paying: {df_bills['days_to_pay'].mean()}')

data_clients = {
    'client_id': [1, 2, 3, 4, 5],
    'balance': [500, 1200, 7000, 2500, 300]
}
df_clients = pd.DataFrame(data_clients)
bns = [0,1000,5000,float('inf')]
labels = ['Silver','Gold','Platinum']

df_clients['Segment'] = pd.cut(df_clients['balance'], bins= bns, labels=labels,right=False)


print(df_clients.value_counts())

#____________________________________________________________________________________________________
