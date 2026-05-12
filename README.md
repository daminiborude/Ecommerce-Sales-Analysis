# 📊 E-Commerce Sales Analysis

An end-to-end Data Analytics project built using **Python, SQL, and Power BI** to analyze e-commerce sales performance, customer behavior, product trends, and regional revenue insights.

---

# 🚀 Project Overview

This project simulates a real-world e-commerce business scenario where sales data is generated, cleaned, analyzed, stored in a star-schema database, and visualized through an interactive Power BI dashboard.

The project covers the complete analytics workflow:

- Data Generation
- Data Cleaning & Feature Engineering
- Exploratory Data Analysis (EDA)
- SQL Data Warehousing & Analytics
- Power BI Dashboard Development
- Business Insights & Recommendations

---

# 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, cleaning, EDA |
| Pandas & NumPy | Data manipulation |
| Matplotlib & Seaborn | Visualization |
| PostgreSQL | Database & SQL analysis |
| SQL | Data modeling & business queries |
| Power BI | Dashboard & KPI reporting |

---

# 📁 Project Structure

```bash
SALES_ANALYTICS/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   └── products.csv
│   │
│   └── cleaned/
│       ├── dim_customers.csv
│       ├── dim_date.csv
│       ├── dim_products.csv
│       └── fact_orders.csv
│
├── powerBI/
│   └── Dashboard.pbix
│
├── python/
│   ├── clean_data.py
│   ├── db_connection.py
│   ├── eda_visuals.py
│   ├── generate_data.py
│   ├── load_data_db.py
│   └── requirements.txt
│
├── report/
│
├── sql/
│   └── schemas.sql
│
└── README.md
```

---

# 📌 Features

## ✅ Data Generation
- Generated 50,000+ realistic e-commerce orders
- Created synthetic customers and product datasets
- Simulated seasonal sales trends

## ✅ Data Cleaning
- Removed duplicate records
- Handled missing values
- Removed invalid rows
- Outlier detection using IQR method
- Feature engineering for time analysis

## ✅ Exploratory Data Analysis
Generated professional EDA charts:
- Monthly Revenue Trend
- Revenue by Category
- Pareto Analysis (80/20 Rule)
- Profit Margin Distribution
- Region vs Quarter Heatmap
- Payment Method Distribution

## ✅ SQL Analytics
Implemented:
- Star Schema Design
- Fact & Dimension Tables
- Window Functions
- CTEs
- RFM Customer Segmentation
- Rolling 3-Month Revenue Analysis
- Regional Performance Analysis

## ✅ Power BI Dashboard
Interactive dashboard with:
- KPI Cards
- Revenue Trends
- Category Performance
- Regional Analysis
- Customer Segmentation
- Time Intelligence DAX Measures
- Drill-through Reports
- Dynamic Filters & Slicers

---

# 📊 Key Insights

- Top 20% customers generated nearly 80% of revenue
- Q4 contributed highest yearly sales
- Electronics category generated maximum revenue
- Books category had highest profit margin
- West region showed higher return rates
- Seasonal demand spike observed during Oct–Dec

---

# 📈 Dashboard Highlights

### KPIs
- Total Revenue
- Total Profit
- Total Orders
- Average Order Value
- Profit Margin %

### Visuals
- Revenue Trend Line Chart
- Revenue by Category Bar Chart
- Regional Heatmap
- Customer Segment Donut Chart
- Top Products Table

---

# 🧠 SQL Concepts Used

- CTEs
- Window Functions
- RANK()
- LAG()
- NTILE()
- Conditional Aggregation
- Rolling Average
- Subqueries
- Views

---

# 📌 Python Concepts Used

- Data Cleaning
- Feature Engineering
- Data Validation
- EDA
- Statistical Analysis
- Visualization

---

# ⚡ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/daminiborude/Ecommerce-Sales-Analysis.git
cd Ecommerce-Sales-Analysis
```

## 2️⃣ Install Dependencies

```bash
pip install -r python/requirements.txt
```

## 3️⃣ Run Python Files

```bash
python python/generate_data.py
python python/clean_data.py
python python/load_data_db.py
python python/eda_visuals.py
```

## 4️⃣ Execute SQL Schema

Run:

```sql
sql/schemas.sql
```

in PostgreSQL / pgAdmin.

## 5️⃣ Open Power BI Dashboard

Open:

```bash
powerBI/Dashboard.pbix
```

---

# 💡 Future Improvements

- Deploy dashboard to Power BI Service
- Add real-time streaming analytics
- Integrate machine learning forecasting
- Build automated ETL pipelines

---

# ⭐ If you like this project, give it a star on GitHub!
