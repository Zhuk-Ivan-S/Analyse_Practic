import numpy as np
import  pandas as pd
import matplotlib.pyplot as plt
import sqlite3

from pandas.io.common import file_exists

df = pd.read_csv('../Row_files/world food production.csv')
#print(df.head(10))
#print(df.isnull().sum())
#print(df.describe())
#print(df.size)
#print(df.info)
#print(df.duplicated().sum())
print(df.columns)

df = df.rename(columns = {'Maize Production (tonnes)':'Maize',
       'Rice  Production ( tonnes)':'Rice', 'Yams  Production (tonnes)':'Yams',
       'Wheat Production (tonnes)':'Wheat', 'Tomatoes Production (tonnes)':'Tomatoes',
       'Tea  Production ( tonnes )':'Tea', 'Sweet potatoes  Production (tonnes)':'Sweet_Potato',
       'Sunflower seed  Production (tonnes)':'Sunflower', 'Sugar cane Production (tonnes)':'Sugar',
       'Soybeans  Production (tonnes)':'Soybeans', 'Rye  Production (tonnes)':'Rye',
       'Potatoes  Production (tonnes)':'Potatoes', 'Oranges  Production (tonnes)':'Oranges',
       'Peas, dry Production ( tonnes)':'Peas', 'Palm oil  Production (tonnes)':'Palm_Oil',
       'Grapes  Production (tonnes)':'Grapes', 'Coffee, green Production ( tonnes)':'Coffee',
       'Cocoa beans Production (tonnes)':'Cocoa', 'Meat, chicken  Production (tonnes)':'Meat',
       'Bananas  Production ( tonnes)':'Bananas', 'Avocados Production (tonnes)':'Avocados',
       'Apples Production (tonnes)':'Apples'})
print(df.columns)

# print(df['Entity'].unique())
# Отже тут можна відсортувати групи країн або регіони обєднання і так далі методом створення нового дата фрейму де просто
# дропнути обєнання , континенти і так далі і залишити виключно країни
regions_to_drop = ['World', 'Africa', 'Asia', 'Europe', 'South America',
                   'North America', 'European Union', 'Oceania', 'Low income food deficit countries']

df = df[~df['Entity'].isin(regions_to_drop)]
top_culture = df[['Maize', 'Rice', 'Yams', 'Wheat', 'Tomatoes', 'Tea',
       'Sweet_Potato', 'Sunflower', 'Sugar', 'Soybeans', 'Rye', 'Potatoes',
       'Oranges', 'Peas', 'Palm_Oil', 'Grapes', 'Coffee', 'Cocoa', 'Meat',
       'Bananas', 'Avocados', 'Apples']].sum().sort_values(ascending=False)
print(top_culture.head(3))
# Top 3 culture are Sugar Wheat and Rice

top_culture_year = df.groupby('Year')[['Sugar','Wheat','Rice']].sum()
print(top_culture_year)


#top_culture_year.plot(kind = 'line')
#plt.show()

# в загальному спостерігається поступове падіння виробництва протягом 1960 року до 1990 потім зростання особливо в Wheat
# and Rice . Sugar також притримується даної тенденції можна виділити "найгірші та найкращі роки " з мінімальними та мак
# симальні показники врожайності наприклад 2011 для цукру ...
data_2021 = df[df['Year'] == 2021]
print(data_2021)
top_wheat_prod = data_2021.groupby('Entity')['Wheat'].sum().sort_values(ascending = False)
print(top_wheat_prod.head(10))

#top_wheat_prod.head(10).plot(kind='bar')
#plt.show()

top_cocoa = data_2021.groupby('Entity')['Cocoa'].sum().sort_values(ascending = False)

print(top_cocoa.head(10))
#top_cocoa.head(10).plot(kind = 'bar')
#plt.show()

# з точки зору аналізу виробництво цих продуктів є абсолютно кліматичним , задача полягала в визначенні топ країн які
#виробляють продукти арчування різних типів за 2021 рік і за висновком культура какао боби та пшениця є регіональними
#та обєм виробництва залежить від клімату на мою думку

crops = ['Maize', 'Rice', 'Yams', 'Wheat', 'Tomatoes', 'Tea',
       'Sweet_Potato', 'Sunflower', 'Sugar', 'Soybeans', 'Rye', 'Potatoes',
       'Oranges', 'Peas', 'Palm_Oil', 'Grapes', 'Coffee', 'Cocoa', 'Meat',
       'Bananas', 'Avocados', 'Apples']
df['Total_production'] = df[crops].sum(axis = 1)
print(df['Total_production'])

top_countries_by_prod  = df.groupby('Entity')['Total_production'].sum().sort_values(ascending = False)
print(top_countries_by_prod.head(10))

#top_countries_by_prod.head(10).plot(kind= 'bar')
#plt.show()
data_2021 = df[df['Year'] == 2021]
data_1961 = df[df['Year'] == 1961]

difference = ((data_2021.groupby('Entity')['Total_production'].sum() - data_1961.groupby('Entity')['Total_production'].sum())/data_1961.groupby('Entity')['Total_production'].sum()) *100
print(f'Percentage grow : {difference.sort_values(ascending = False).head(10)} %')
difference = difference.dropna()
print(difference.sort_values(ascending = False).tail(10))


conn = sqlite3.connect('../food_database.db')
df.to_sql('production',conn, if_exists= 'replace', index = False)

query = '''SELECT Entity, Sum(Rice) as Total_Rice from production WHERE Year = 2021 Group by Entity Order by Total_Rice DESC Limit 10'''
df_rice = pd.read_sql_query(query, conn)
print(df_rice)

query = '''SELECT Entity from production GROUP BY Entity HAVING Count(Year) = 61;'''
df_clear = pd.read_sql_query(query,conn)
print(df_clear)

sugar= '''SELECT 
    t2021.Entity, 
    t1990.Sugar as Sugar_1990, 
    t2021.Sugar as Sugar_2021,
    (t2021.Sugar - t1990.Sugar) as Absolute_Growth
FROM 
    (SELECT Entity, Sugar FROM production WHERE Year = 2021) as t2021
JOIN 
    (SELECT Entity, Sugar FROM production WHERE Year = 1990) as t1990 
ON 
    t2021.Entity = t1990.Entity
ORDER BY 
    Absolute_Growth DESC
LIMIT 10;'''
df_sugar_2021 = pd.read_sql_query(sugar, conn)
print(df_sugar_2021.head(10))



query = '''SELECT Entity, SUM(Total_production) as Grand_Total
FROM production
GROUP BY Entity
HAVING Grand_Total > 1000000000
ORDER BY Grand_Total DESC;'''
df_top_giants = pd.read_sql_query(query, conn)
print(df_top_giants)