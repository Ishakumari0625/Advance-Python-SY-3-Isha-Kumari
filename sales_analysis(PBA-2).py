# Sales Data Analysis using Pandas and Matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv("sales.csv")

# Display total and average sales
print("Total Sales:", df["Sales"].sum())
print("Average Sales:", df["Sales"].mean())

# Find month with highest sales
print("Highest Sales Month:", df.loc[df["Sales"].idxmax(), "Month"])

# Group sales by product category
category_sales = df.groupby("Category")["Sales"].sum()
print(category_sales)

# Bar chart - Category-wise sales
category_sales.plot(kind="bar", title="Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.show()

# Line chart - Monthly sales trend
monthly_sales = df.groupby("Month")["Sales"].sum()
monthly_sales.plot(kind="line", marker="o", title="Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Pie chart - Category contribution
category_sales.plot(kind="pie", autopct="%1.1f%%", title="Category-wise Sales")
plt.ylabel("")
plt.show()