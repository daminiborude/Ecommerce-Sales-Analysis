# clean_data.py

import pandas as pd
import numpy as np
import os

os.makedirs("data/cleaned", exist_ok=True)

# LOAD DATA
orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date"])
customers = pd.read_csv("data/raw/customers.csv", parse_dates=["join_date"])
products = pd.read_csv("data/raw/products.csv")

print("=== RAW DATA QUALITY REPORT ===")
print(f"Orders: {len(orders):,} rows | Nulls: {orders.isnull().sum().sum()}")
print(f"Customers: {len(customers):,} rows | Nulls: {customers.isnull().sum().sum()}")
print(f"Products: {len(products):,} rows | Nulls: {products.isnull().sum().sum()}")

# ── STEP 1: REMOVE FULL DUPLICATES
before = len(orders)
orders = orders.drop_duplicates()
print(f"\n✅ Full duplicates removed: {before - len(orders)}")

# ── STEP 2: REMOVE INVALID ROWS FIRST
before = len(orders)
orders = orders[orders["quantity"] > 0]
orders = orders[orders["unit_price"] > 0]
orders = orders[orders["status"] != "Processing"]
print(f"✅ Invalid rows removed: {before - len(orders)}")

# ── STEP 3: HANDLE MISSING VALUES
null_rev_mask = orders["revenue"].isnull()

orders.loc[null_rev_mask, "revenue"] = (
    orders.loc[null_rev_mask, "unit_price"] *
    orders.loc[null_rev_mask, "quantity"] *
    (1 - orders.loc[null_rev_mask, "discount_pct"] / 100)
).round(2)

print(f"✅ Revenue nulls imputed: {null_rev_mask.sum()}")

# ── STEP 4: OUTLIER DETECTION (FAST)
Q1 = orders["revenue"].quantile(0.25)
Q3 = orders["revenue"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 3 * IQR
upper = Q3 + 3 * IQR

orders["is_outlier"] = ((orders["revenue"] < lower) | (orders["revenue"] > upper)).astype(int)

print(f"⚠️ Outliers flagged between ₹{lower:,.0f} – ₹{upper:,.0f}")

# ── STEP 5: FEATURE ENGINEERING
orders["year"] = orders["order_date"].dt.year
orders["month"] = orders["order_date"].dt.month
orders["month_name"] = orders["order_date"].dt.strftime("%B")
orders["quarter"] = orders["order_date"].dt.quarter
orders["quarter_label"] = "Q" + orders["quarter"].astype(str)
orders["week"] = orders["order_date"].dt.isocalendar().week.astype(int)
orders["day_of_week"] = orders["order_date"].dt.day_name()
orders["is_weekend"] = orders["order_date"].dt.dayofweek >= 5

# Safe profit margin
orders["profit_margin"] = np.where(
    orders["revenue"] > 0,
    (orders["profit"] / orders["revenue"]) * 100,
    0
).round(2)

orders["is_discounted"] = orders["discount_pct"] > 0

orders["revenue_band"] = pd.cut(
    orders["revenue"],
    bins=[0, 500, 2000, 10000, float("inf")],
    labels=["Low (<₹500)", "Medium (₹500-2K)", "High (₹2K-10K)", "Premium (>₹10K)"]
)

print("✅ Feature engineering completed")

# ── STEP 6: MERGE (FACT TABLE)
fact = (
    orders.merge(customers[["customer_id", "region", "segment", "city"]],
                 on="customer_id", how="left")
          .merge(products[["product_id", "category", "brand"]],
                 on="product_id", how="left")
)

# ── STEP 7: SAVE FILES
fact.to_csv("data/cleaned/fact_orders.csv", index=False)
customers.to_csv("data/cleaned/dim_customers.csv", index=False)
products.to_csv("data/cleaned/dim_products.csv", index=False)

# DATE DIMENSION
date_range = pd.date_range(start="2022-01-01", end="2024-12-31")

dim_date = pd.DataFrame({
    "date": date_range,
    "year": date_range.year,
    "quarter": date_range.quarter,
    "month": date_range.month,
    "month_name": date_range.strftime("%B"),
    "week": date_range.isocalendar().week.astype(int),
    "day": date_range.day,
    "day_name": date_range.day_name(),
    "is_weekend": date_range.dayofweek >= 5,
    "is_month_end": date_range.is_month_end,
})

dim_date.to_csv("data/cleaned/dim_date.csv", index=False)

print("\n✅ Cleaned data saved successfully")









































# import pandas as pd
# import numpy as np
# import os

# os.makedirs("data/cleaned", exist_ok=True)

# # LOAD RAW DATA
# orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date"])
# customers = pd.read_csv("data/raw/customers.csv", parse_dates=["join_date"])
# products = pd.read_csv("data/raw/products.csv")

# print("=== RAW DATA QUALITY REPORT ===")
# print(f"Orders: {len(orders):,} rows | Nulls: {orders.isnull().sum().sum()}")
# print(f"Customers: {len(customers):,} rows | Nulls: {customers.isnull().sum().sum()}")
# print(f"Products: {len(products):,} rows | Nulls: {products.isnull().sum().sum()}")

# # STEP 1 — REMOVE DUPLICATES
# before = len(orders)
# orders.drop_duplicates(subset=["order_id"], inplace=True)
# print(f"\n✅ Duplicates removed: {before - len(orders)}")

# # STEP 2 — HANDLE MISSING VALUES
# null_rev_mask = orders["revenue"].isnull()
# orders.loc[null_rev_mask, "revenue"] = (
#     orders.loc[null_rev_mask, "unit_price"] *
#     orders.loc[null_rev_mask, "quantity"] *
#     (1 - orders.loc[null_rev_mask, "discount_pct"] / 100)
# ).round(2)
# print(f"✅ Revenue nulls imputed: {null_rev_mask.sum()}")

# # STEP 3 — REMOVE INVALID ROWS
# before = len(orders)
# orders = orders[orders["quantity"] > 0]
# orders = orders[orders["revenue"] > 0]
# orders = orders[orders["status"] != "Processing"]
# print(f"✅ Invalid rows removed: {before - len(orders)}")

# # STEP 4 — OUTLIER DETECTION
# Q1 = orders["revenue"].quantile(0.25)
# Q3 = orders["revenue"].quantile(0.75)
# IQR = Q3 - Q1
# lower = Q1 - 3 * IQR
# upper = Q3 + 3 * IQR

# orders["is_outlier"] = orders["revenue"].apply(
#     lambda x: 1 if x < lower or x > upper else 0
# )

# print(f"⚠️ Outliers flagged between ₹{lower:,.0f} – ₹{upper:,.0f}")

# # STEP 5 — FEATURE ENGINEERING
# orders["year"] = orders["order_date"].dt.year
# orders["month"] = orders["order_date"].dt.month
# orders["month_name"] = orders["order_date"].dt.strftime("%B")
# orders["quarter"] = orders["order_date"].dt.quarter
# orders["quarter_label"] = "Q" + orders["quarter"].astype(str)
# orders["week"] = orders["order_date"].dt.isocalendar().week
# orders["day_of_week"] = orders["order_date"].dt.day_name()
# orders["is_weekend"] = orders["order_date"].dt.dayofweek >= 5
# orders["profit_margin"] = ((orders["profit"] / orders["revenue"]) * 100).round(2)
# orders["is_discounted"] = orders["discount_pct"] > 0

# orders["revenue_band"] = pd.cut(
#     orders["revenue"],
#     bins=[0, 500, 2000, 10000, float("inf")],
#     labels=["Low (<₹500)", "Medium (₹500-2K)", "High (₹2K-10K)", "Premium (>₹10K)"]
# )

# print("✅ Feature engineering completed")

# # STEP 6 — MERGE
# fact = (
#     orders.merge(customers[["customer_id", "region", "segment", "city"]],
#                  on="customer_id", how="left")
#           .merge(products[["product_id", "category", "brand"]],
#                  on="product_id", how="left")
# )

# # STEP 7 — SAVE FILES
# fact.to_csv("data/cleaned/fact_orders.csv", index=False)
# customers.to_csv("data/cleaned/dim_customers.csv", index=False)
# products.to_csv("data/cleaned/dim_products.csv", index=False)

# # DATE TABLE
# date_range = pd.date_range(start="2022-01-01", end="2024-12-31")
# dim_date = pd.DataFrame({
#     "date": date_range,
#     "year": date_range.year,
#     "quarter": date_range.quarter,
#     "month": date_range.month,
#     "month_name": date_range.strftime("%B"),
#     "week": date_range.isocalendar().week,
#     "day": date_range.day,
#     "day_name": date_range.day_name(),
#     "is_weekend": date_range.dayofweek >= 5,
#     "is_month_end": date_range.is_month_end,
# })

# dim_date.to_csv("data/cleaned/dim_date.csv", index=False)

# print("\n✅ Cleaned data saved successfully")
