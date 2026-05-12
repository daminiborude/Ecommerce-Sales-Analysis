# 01_generate_data.py   

"""
Generates synthetic e-commerce data:
- 50,000 orders over 3 years
- 5,000 customers
- 200 products across 8 categories
- 6 regions across India
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# ── Config
N_ORDERS = 50_000
N_CUSTOMERS = 5_000
N_PRODUCTS = 200

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

CATEGORIES = {
    "Electronics": (5000, 80000),
    "Fashion": (299, 5000),
    "Home & Kitchen": (499, 15000),
    "Books": (99, 1500),
    "Sports": (299, 12000),
    "Beauty": (199, 3000),
    "Toys": (199, 4000),
    "Groceries": (49, 999),
}

REGIONS = ["North", "South", "East", "West", "Central", "Northeast"]
SEGMENTS = ["Premium", "Regular", "Budget"]

# ── Generate Customers
def generate_customers(n):
    cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
              "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Surat"]

    data = {
        "customer_id": [f"CUST{str(i).zfill(5)}" for i in range(1, n+1)],
        "name": [f"Customer_{i}" for i in range(1, n+1)],
        "email": [f"customer{i}@email.com" for i in range(1, n+1)],
        "city": np.random.choice(cities, n),
        "region": np.random.choice(REGIONS, n),
        "segment": np.random.choice(SEGMENTS, n, p=[0.2, 0.5, 0.3]),
        "join_date": [START_DATE + timedelta(days=random.randint(0, 365)) for _ in range(n)],
    }

    return pd.DataFrame(data)


# ── Generate Products
def generate_products(n):
    categories = list(CATEGORIES.keys())

    cat_list = np.random.choice(categories, n)
    prices = np.array([round(random.uniform(*CATEGORIES[c]), 2) for c in cat_list])
    costs = np.round(prices * np.random.uniform(0.4, 0.7, n), 2)

    data = {
        "product_id": [f"PROD{str(i).zfill(4)}" for i in range(1, n+1)],
        "product_name": [f"{cat.split()[0]}_Product_{i}" for i, cat in enumerate(cat_list, 1)],
        "category": cat_list,
        "price": prices,
        "cost": costs,
        "brand": np.random.choice(["BrandA", "BrandB", "BrandC", "BrandD"], n),
    }

    return pd.DataFrame(data)


# ── Generate Orders (OPTIMIZED 🚀)
def generate_orders(n, customers, products):

    cust_ids = customers["customer_id"].values
    prod_ids = products["product_id"].values

    # Dates (vectorized)
    years = np.random.choice([2022, 2023, 2024], n)
    months = np.random.choice(range(1, 13), n,
                             p=np.array([4,3,3,4,4,5,5,6,7,10,12,10]) / 73)
    days = np.random.randint(1, 29, n)

    dates = [datetime(y, m, d) for y, m, d in zip(years, months, days)]

    # Core data
    chosen_prods = np.random.choice(prod_ids, n)
    quantities = np.random.choice([1,1,1,2,2,3,4,5], n)
    discounts = np.random.choice([0,0,0,5,10,15,20], n)

    prod_df = products.set_index("product_id")
    unit_prices = prod_df.loc[chosen_prods, "price"].values
    unit_costs = prod_df.loc[chosen_prods, "cost"].values

    revenues = np.round(unit_prices * quantities * (1 - discounts/100), 2)
    profits = np.round((unit_prices - unit_costs) * quantities * (1 - discounts/100), 2)

    statuses = np.random.choice(
        ["Delivered", "Returned", "Cancelled", "Processing"],
        n,
        p=[0.80, 0.08, 0.07, 0.05]
    )

    payments = np.random.choice(
        ["Credit Card", "UPI", "Debit Card", "NetBanking", "COD"],
        n,
        p=[0.30, 0.35, 0.15, 0.10, 0.10]
    )

    data = {
        "order_id": [f"ORD{str(i).zfill(6)}" for i in range(1, n+1)],
        "customer_id": np.random.choice(cust_ids, n),
        "product_id": chosen_prods,
        "order_date": dates,
        "quantity": quantities,
        "unit_price": unit_prices,
        "unit_cost": unit_costs,
        "discount_pct": discounts,
        "revenue": revenues,
        "profit": profits,
        "status": statuses,
        "payment": payments,
    }

    df = pd.DataFrame(data)

    # ── Data quality issues
    df.loc[df.sample(frac=0.02).index, "revenue"] = np.nan
    df = pd.concat([df, df.sample(frac=0.01)], ignore_index=True)
    df.loc[df.sample(frac=0.005).index, "quantity"] = -1

    return df


# ── Run & Save
os.makedirs("data/raw", exist_ok=True)

customers = generate_customers(N_CUSTOMERS)
products = generate_products(N_PRODUCTS)
orders = generate_orders(N_ORDERS, customers, products)

customers.to_csv("data/raw/customers.csv", index=False)
products.to_csv("data/raw/products.csv", index=False)
orders.to_csv("data/raw/orders.csv", index=False)

print(f"✅ Generated: {len(orders)} orders, {len(customers)} customers, {len(products)} products")
print(f"Nulls in revenue: {orders['revenue'].isnull().sum()}")
print(f"Duplicate rows: {orders.duplicated().sum()}")
print(f"Negative quantity: {(orders['quantity'] < 0).sum()}")


