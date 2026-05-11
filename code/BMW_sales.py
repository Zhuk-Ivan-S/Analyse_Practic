import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

bmw_dataset = pd.read_csv("../Row_files/BMW sales data (2010-2024) (1).csv")
df = pd.DataFrame(bmw_dataset)
print(df.head(10))

def cleaned(dataframe):
    print(dataframe.isnull().sum())
    print(dataframe.duplicated().sum())
    print(dataframe.info())
    print(dataframe.size)

cleaned(df)
df['Total_Sales'] = df['Price_USD'] * df['Sales_Volume']


df['Total_Sales_in_billions'] = df['Total_Sales'] / 1000000000 # in billions of USD
print(df['Total_Sales_in_billions'].head(10))
sales_by_year = df.groupby('Year')['Total_Sales_in_billions'].sum()
# Forecast with Linear Regression

X = df[['Year']]
y = df['Total_Sales_in_billions']

model = LinearRegression()
model.fit(X,y)

prediction_2025 = model.predict(pd.DataFrame({'Year' : [2025]}))
print(f'Prediction of sales in 2025 : {prediction_2025}')

# Visualisation of Forecast

plt.figure(figsize=(12, 6))

plt.plot(sales_by_year.index, sales_by_year.values,
         color='blue', marker='o', linestyle='-', linewidth=2, label='Реальні дані (згруповані)')

plt.plot(df['Year'], model.predict(X),
         color='red', linewidth=3, linestyle='--', label='Лінія тренду (Регресія)')

plt.scatter(2025, prediction_2025, color='green', marker='X', s=200, label='Прогноз 2025')

plt.title('Аналіз та прогноз продажів BMW (Educational Data - Grouped by Year)', fontsize=16)
plt.xlabel('Рік', fontsize=12)
plt.ylabel('Продажі (в млрд $)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.show()
