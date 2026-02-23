import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../Row_files/grocery_chain_data.csv')

print(df.info)
print(df.size)
print(df.duplicated().sum())
print(df.isnull().sum())
print(df.columns)

print(df['transaction_date'].max())

# today is 19.12.2025 thats mean all is good with data

df['Payment_errors'] = np.where(
    df['final_amount'] <= 0, 'Need Attention', 'All is good'
)

print(df['Payment_errors'].value_counts())
print(np.where(df['Payment_errors'] == 'Need Attention'))

# visualisation
top_goods = df.groupby('product_name')['total_amount'].sum().sort_values(ascending= False)
print(top_goods.head(10))

top_goods.plot(kind = 'bar')
plt.show()

correl_client = df[['loyalty_points','total_amount']].corr()
print(correl_client)
# не має залежності від суи покупки та лояльністю клієнтів
correl_discount = df[['discount_amount','loyalty_points']].corr()
print(correl_discount)

# відсутня залежність

top_10_clients_by_amount = df.groupby('customer_id')['total_amount'].sum().sort_values(ascending = False).head(10)
print(top_10_clients_by_amount)

top_10_clients_by_amount.plot(kind = 'bar')
plt.show()
#22860 !!!
top_shops = df.groupby('store_name')['total_amount'].mean().sort_values(ascending=False).head(10)
print(top_shops)
plt.figure(figsize=(10,8))
top_shops.plot(kind = 'pie', autopct = '%1.1f%%')
plt.legend(loc = 'upper left')
plt.show()

top_good_in_shop = df.groupby('store_name')['aisle'].value_counts()
print(top_good_in_shop)

top_good_in_shop.plot(kind = 'area')
plt.xticks(rotation = 90)
plt.show()
# Place most of
print(df['aisle'].value_counts())


