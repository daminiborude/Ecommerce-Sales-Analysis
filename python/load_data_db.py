import pandas as pd
from db_connection import engine

# Load data
fact = pd.read_csv("data/cleaned/fact_orders.csv")
customers = pd.read_csv("data/cleaned/dim_customers.csv")
products = pd.read_csv("data/cleaned/dim_products.csv")
date_dim = pd.read_csv("data/cleaned/dim_date.csv")

# Upload
fact.to_sql("fact_orders", engine, if_exists="replace", index=False)
customers.to_sql("dim_customers", engine, if_exists="replace", index=False)
products.to_sql("dim_products", engine, if_exists="replace", index=False)
date_dim.to_sql("dim_date", engine, if_exists="replace", index=False)

print("✅ Data loaded into MySQL!")