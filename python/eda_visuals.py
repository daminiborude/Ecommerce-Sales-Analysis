import pandas as pd
import matplotlib.pyplot as plt
import os

# Create folder
os.makedirs("report/charts", exist_ok=True)

# Load data
fact = pd.read_csv("data/cleaned/fact_orders.csv", parse_dates=["order_date"])

# ─────────────────────────────────────────────
# Pre-compute (IMPORTANT for speed)
# ─────────────────────────────────────────────
fact["year"] = fact["order_date"].dt.year
fact["month"] = fact["order_date"].dt.month

monthly = fact.groupby(["year", "month"], as_index=False)["revenue"].sum()
cat_rev = fact.groupby("category", as_index=False)["revenue"].sum()
cust_rev = fact.groupby("customer_id")["revenue"].sum().sort_values(ascending=False)

# ─────────────────────────────────────────────
# Chart 1: Monthly Trend
# ─────────────────────────────────────────────
plt.figure(figsize=(10, 4))

for y in sorted(monthly["year"].unique()):
    subset = monthly[monthly["year"] == y]
    plt.plot(subset["month"], subset["revenue"]/1e6, marker="o", label=str(y))

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹ Million)")
plt.legend()
plt.tight_layout()
plt.savefig("report/charts/01_trend.png")
plt.close()

# ─────────────────────────────────────────────
# Chart 2: Category Revenue
# ─────────────────────────────────────────────
plt.figure(figsize=(8, 5))

plt.barh(cat_rev["category"], cat_rev["revenue"]/1e6)

plt.title("Revenue by Category")
plt.xlabel("₹ Million")
plt.tight_layout()
plt.savefig("report/charts/02_category.png")
plt.close()

# ─────────────────────────────────────────────
# Chart 3: Pareto (OPTIMIZED)
# ─────────────────────────────────────────────
# Use only top 1000 customers for speed
cust_rev_top = cust_rev.head(1000)

cumulative = cust_rev_top.cumsum() / cust_rev_top.sum() * 100

plt.figure(figsize=(10, 4))
plt.plot(cumulative.values)

plt.axhline(80, linestyle="--")
plt.title("Pareto (Top 1000 Customers)")
plt.ylabel("Cumulative %")
plt.tight_layout()
plt.savefig("report/charts/03_pareto.png")
plt.close()

# ─────────────────────────────────────────────
# Chart 4: Profit Margin (Sampled for speed)
# ─────────────────────────────────────────────
sample = fact.sample(5000)

plt.figure(figsize=(8, 5))
plt.boxplot(sample["profit_margin"])

plt.title("Profit Margin Distribution")
plt.tight_layout()
plt.savefig("report/charts/04_margin.png")
plt.close()

# ─────────────────────────────────────────────
# Chart 5: Region vs Quarter (FAST VERSION)
# ─────────────────────────────────────────────
pivot = fact.groupby(["region", "quarter_label"])["revenue"].sum().unstack()

plt.figure(figsize=(8, 5))
plt.imshow(pivot, aspect="auto")

plt.title("Region vs Quarter Heatmap")
plt.colorbar()
plt.tight_layout()
plt.savefig("report/charts/05_heatmap.png")
plt.close()

# ─────────────────────────────────────────────
# Chart 6: Payment Method
# ─────────────────────────────────────────────
pay_counts = fact["payment"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%")

plt.title("Payment Methods")
plt.tight_layout()
plt.savefig("report/charts/06_payment.png")
plt.close()

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
print("\n✅ EDA charts generated FAST")
print(f"Total Orders  : {len(fact):,}")
print(f"Revenue       : ₹{fact['revenue'].sum():,.0f}")
print(f"Profit        : ₹{fact['profit'].sum():,.0f}")
print(f"Top Category  : {cat_rev.sort_values('revenue', ascending=False).iloc[0]['category']}")

