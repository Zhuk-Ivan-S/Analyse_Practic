import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_csv('../Row_files/vgsales.csv')
print(df.head(10))
print(df.columns)
print('Size of dataset:',df.size)
print('Mising values:', df.isnull().value_counts())
print('Duplicates:' , df.duplicated().value_counts())

conn = sqlite3.connect('databaseVGsales.db')
df.to_sql('vgsales',conn, if_exists="replace", index=False)

# Now we have some possibilities to manipulate data in SQL - for example choose Top of games sort, group, Case , clean
# with Replace and so on
# For example, let's take the best games of all time and other features

query = '''SELECT Name, Year, Genre ,Global_Sales from vgsales ORDER BY Global_Sales DESC LIMIT 10;'''
df_top_games = pd.read_sql_query(query, conn)
print(df_top_games)
# or which genre brings in more revenue

query = '''SELECT Genre, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales from vgsales GROUP BY Genre Order by 
            Global_sales DESC LIMIT 10'''
df_genre_rev = pd.read_sql_query(query,conn)
print(df_genre_rev)

# This way, we can determine the market and demand in different regions, we can observe that the Sports genre is more
# popular in the European and North American regions, while the Asian market prefers Role-playing games.

# Here some info about Platforms and count of games in different Genre
query = '''SELECT Platform, COUNT(Platform) AS Count_of_products from vgsales GROUP BY Platform ORDER BY Count_of_products DESC LIMIT 10'''
df_platform = pd.read_sql_query(query, conn)
print(df_platform)

# Thats is so easy but we cat find some insights. For example Identifying market leaders each year. Helps understand
# which platform had the most impact at its peak

query = '''SELECT Year, Platform, Sum(Global_Sales) AS Yearly_sales, Rank() OVER(PARTITION BY Year ORDER BY SUM(Global_Sales)
            DESC) AS Sales_Rank_b_year from vgsales  WHERE Year IS NOT NULL GROUP BY Year, Platform ORDER BY Year DESC,
            Sales_Rank_b_Year ASC;'''
df_peak_pl = pd.read_sql_query(query,conn)
print(df_peak_pl)

# top of Publisher by Revenue or count of products , Best Product for every Publisher which brings more Revenue
query = '''SELECT Publisher, Name , Global_Sales from vgsales GROUP BY Publisher HAVING MAX(Global_Sales); '''
df_best_game_publ = pd.read_sql_query(query,conn)
print(df_best_game_publ)

query = '''SELECT Publisher, SUM(Global_Sales) AS Total_Revenue from vgsales GROUP BY Publisher ORDER BY Total_Revenue DESC LIMIT 10'''
df_tot_rev = pd.read_sql_query(query,conn)
print(df_tot_rev)

# For work is important some visualisations. firs of all for understanding
# For example
plt.bar(df_tot_rev['Publisher'], df_tot_rev['Total_Revenue'], color = 'gold')
plt.ylabel('Total Revenue')
plt.xlabel('Company name')
plt.title('Top 10 Companies in game industry be Total Revenue of all time')
plt.xticks(rotation = 90)
plt.show()
