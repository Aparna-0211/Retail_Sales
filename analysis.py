import pandas as pd
import sqlite3

print("🚀 Starting Data Processing...")

# Load dataset
df = pd.read_csv("online_retail.csv", encoding='ISO-8859-1')

print("✅ Data loaded")

# ---------------------------
# 🔹 Data Cleaning
# ---------------------------
df = df.dropna()
df = df.drop_duplicates()

# Convert date column
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Remove negative or zero values
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# ---------------------------
# 🔹 Feature Engineering
# ---------------------------
df['TotalSales'] = df['Quantity'] * df['UnitPrice']
df['Month'] = df['InvoiceDate'].dt.month
df['Year'] = df['InvoiceDate'].dt.year

print("✅ Data cleaned & features created")

# ---------------------------
# 🔹 Store in SQL
# ---------------------------
conn = sqlite3.connect("database.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

print("✅ Data stored in SQL")

# ---------------------------
# 🔹 Basic Analysis
# ---------------------------
print("\n🏆 Top 5 Products:")
print(df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(5))

print("\n🌍 Sales by Country:")
print(df.groupby('Country')['TotalSales'].sum().sort_values(ascending=False).head(5))

# ---------------------------
# 🔹 Export to Excel
# ---------------------------
df.to_excel("final_report.xlsx", index=False)

print("\n🎉 DONE! Ready for dashboard")