import pandas as pd
import numpy as np

# Setup parameters
dates = pd.date_range(start="1970-01-01", end="2025-12-31")
regions = ['North America', 'Europe', 'Asia', 'South America']
products = ['Smartwatch', 'Tablet', 'Laptop', 'Wireless Earbuds']
prices = {'Smartwatch': 299, 'Tablet': 499, 'Laptop': 999, 'Wireless Earbuds': 149}

data = []

for date in dates:
    for region in regions:
        # Cycle through products so each region has one sale entry per day
        prod = np.random.choice(products)
        base_price = prices[prod]
        
        # Add some "noise" to units sold based on time of year (holiday peak)
        seasonality = 1.5 if date.month == 12 else 1.0
        units = int(np.random.randint(40, 500) * seasonality)
        
        revenue = units * base_price
        rating = round(np.random.uniform(3.5, 5.0), 1)
        
        data.append([date.strftime('%Y-%m-%d'), region, prod, units, base_price, revenue, rating])

# Create DataFrame and Save
df = pd.DataFrame(data, columns=['Date', 'Region', 'Product', 'Units_Sold', 'Unit_Price', 'Revenue', 'Customer_Rating'])
df.to_csv("large_sales_data_2025.csv", index=False)

print(f"File created with {len(df)} rows.")