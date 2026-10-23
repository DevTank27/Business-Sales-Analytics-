import pandas as pd
import random

start_date = "2022-01-01"
end_date   = "2025-12-31"

outlets = ["Outlet_A", "Outlet_B", "Outlet_C", "Outlet_D", "Outlet_E"]

products = [
    ("P101", "iPhone 13", "Electronics", 70000),
    ("P102", "Samsung TV", "Electronics", 45000),
    ("P103", "Dell Laptop", "Electronics", 60000),
    ("P201", "Sofa", "Furniture", 30000),
    ("P202", "Dining Table", "Furniture", 40000),
    ("P301", "T-Shirt", "Clothing", 800),
    ("P302", "Jeans", "Clothing", 1500),
    ("P401", "Milk 1L", "Grocery", 50),
    ("P402", "Rice 5kg", "Grocery", 300),
    ("P403", "Bread", "Grocery", 40),
]

dates = pd.date_range(start_date, end_date, freq="D")

rows = []

for date in dates:
    for outlet in outlets:

        daily_products = random.sample(products, random.randint(3, 6))

        for pid, name, category, price in daily_products:
            qty = random.randint(1, 25)

            rows.append([
                date.strftime("%Y-%m-%d"),
                pid,
                name,
                category,
                outlet,
                qty,
                price
            ])

df = pd.DataFrame(rows, columns=[
    "date", "product_id", "product_name",
    "category", "outlet", "quantity", "unit_price"
])

df.to_csv("sales_data.csv", index=False)

print("CSV generated successfully!")
print("Total rows:", len(df))
