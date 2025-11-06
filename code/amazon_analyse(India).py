import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('../Row_files/amazon.csv')

print('First 10 rows: ',df.head(10))
print('Size of dataset: ',df.size)
print('describe:',df.info())
print('Count of info:' ,df.value_counts())
print('Duplicates: ',df.duplicated())
print('Missing values: ', df.isnull().sum())


print(df.columns)
print(df['discounted_price'].head(10))
# Some signs '₹' in discount price and actual price  - replace that and change from str to float

df['discounted_price'] = df['discounted_price'].str.replace('₹','')
df['discounted_price'] = df['discounted_price'].str.replace(',','') # error (consist coma in values)
df['discounted_price'] = df['discounted_price'].astype(float)
df['actual_price'] = df['actual_price'].str.replace('₹','')
df['actual_price'] = df['actual_price'].str.replace(',','')
df['actual_price'] = df['actual_price'].astype(float)
df['rating'] = df['rating'].replace('|','')
df['rating'] = df['rating'].replace('',np.nan)
df['rating'] = df['rating'].fillna(0)
df['rating'] = df['rating'].astype(float)
df['rating_count'] = df['rating_count'].str.replace(',','')
df['rating_count'] = df['rating_count'].replace('',np.nan)
df['rating_count'] = df['rating_count'].fillna(0)
df['rating_count'] = df['rating_count'].astype(float)
print(df['discounted_price'].head(10))
print(df['actual_price'].head(10))

print(df['discount_percentage'].head(10))
df['discount_percentage'] = df['discount_percentage'].str.replace('%','').astype(float) / 100
print(df['discount_percentage'])

print(df['category'].nunique())
#print(df['category'].unique())
print(df['product_name'].sort_values().head(10))

# find mistakes in discount percentage if they exist
df['discount_perc_fact'] = (1 - df['discounted_price']/df['actual_price']) * 100
print(df['discount_perc_fact'].round())
print(df['discount_percentage'].round(2)*100)
are_equal = df['discount_percentage'].round(2).equals(df['discount_perc_fact'].round()*100)
# logic anomalies
#df['price_anomaly'] = (df['actual_price'] - df['discounted_price'])
#for n in df['price_anomaly']:
   # if n >= 0:
    #    print('No anomaly')
    #else: print('Exist some errors')

print(are_equal)
df['d_p'] = df['discount_percentage'].round(2) * 100
df['d_p_f'] = df['discount_perc_fact'].round()
difference = df.loc[df['d_p'] != df['d_p_f']]
print(difference.value_counts().count())
# some differences between actual discount and discount in database

# make some EDA
# count of unique products
print(f'Count of unique products on Market:{df['product_name'].nunique()}')
# count of categories
print(f'Count of unique Categories on Market: {df['category'].nunique()}')
# Average rating
print(f'Average rating of products on Market: {df['rating'].mean().round(2)}')
# average price , average discount and average discount cost
print(f'Average actual price: {df['actual_price'].mean()}₹' )
print(f'Average discounted price: {df['discounted_price'].mean()}₹')
print(f'Average discount cost: {df['actual_price'].mean() - df['discounted_price'].mean()}₹')
# So, if I started by identifying discounts and looking for inconsistencies, the question arises how much
# "price aggression" costs the company
price_aggression = df['actual_price'].sum() - df['discounted_price'].sum()
print(f'Price Aggression:  {price_aggression.round(2)} ₹')
print(f'loss of margin: {(price_aggression/df['actual_price'].sum()).round(2) * 100} %')

# Top of categories in different sort values
top_10_by_rating = df.groupby('category')['rating'].mean().sort_values(ascending=False).reset_index()
print(top_10_by_rating.head(10))
top_10_exp_cat = df.groupby('category')['actual_price'].max().sort_values(ascending=False).reset_index()
print(top_10_exp_cat.head(10))
# Top 10 categories with most revenue
top_10_rev = df.groupby('category')['discounted_price'].sum().sort_values(ascending= False).reset_index()
print(top_10_rev.head(10))
# most Categories on Market
Top_10_count_cat = df.groupby('category')['product_id'].count().sort_values(ascending=False).reset_index()
print(Top_10_count_cat.head(10))

# We can find other rating values for example by count of reviews or price aggression ...

# Analyse of ratings and reviews
plt.figure(figsize=(8,7))
plt.hist(df['rating'])
plt.xlabel('Rating on Market')
plt.ylabel('Count of reviews')
plt.show()
# most of all 4.0 - 4.5 (1000) reviews

corel_rat_disc = df[['rating','discount_percentage']].corr()
corel_rat_actp = df[['rating','actual_price']].corr()
corel_rat_count_discp = df[['rating_count','discounted_price']].corr()
print(corel_rat_disc)
print(corel_rat_actp)
print(corel_rat_count_discp)

# Correlation analyse
sns.heatmap(df[['rating','actual_price','discount_percentage','rating_count']].corr())
plt.show()
# percent of unique customers and repeat
perc_unique = df['user_id'].nunique()
print(f'Unique (new) customers: {perc_unique}')
# Visual EDA
plt.scatter(x = df['discount_percentage'], y = df['rating'], color = 'blue')
plt.show()
# rating does not depend on the  discount percentage
plt.scatter(x= df['rating_count'], y = df['discounted_price'], color = 'red')
plt.show()
# Low costed products have more reviews and rating count
plt.hist(Top_10_count_cat.head(10))
plt.xticks(rotation = 90)
plt.show()

df.to_csv('../Final_files(clean, prepared or some visualisation)/amazon_1.csv')
