import numpy as np
import  pandas as pd
import matplotlib.pyplot as plt
import sqlite3


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
