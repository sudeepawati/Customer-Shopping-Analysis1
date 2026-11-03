"""
Customer Shopping Data Analysis & Cleaning Pipeline - Indian Retail Edition
Technologies: Python, Pandas, NumPy, Matplotlib, Seaborn
Currency: Indian Rupee (₹ - INR)
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def format_inr(number):
    """Formats a number in Indian Rupee format e.g. ₹1,45,200.00"""
    return f"₹{number:,.2f}"

def run_analysis(csv_file='data.csv', output_charts_dir='charts'):
    if not os.path.exists(csv_file):
        print(f"Error: Dataset '{csv_file}' not found. Please run 'python generate_data.py' first.")
        return None

    try:
        import pandas as pd
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        print(f"Required library missing: {e}")
        print("Please install requirements using: pip install -r requirements.txt")
        return None

    os.makedirs(output_charts_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

    print("=" * 70)
    print(" CUSTOMER SHOPPING ANALYSIS - INDIAN RETAIL DATA PIPELINE")
    print("=" * 70)

    # 1. Load Raw Dataset
    raw_df = pd.read_csv(csv_file)
    initial_rows = len(raw_df)
    print(f"\n[1] Loaded Dataset: {initial_rows} records across {len(raw_df.columns)} columns.")

    # 2. Data Cleaning
    print("\n[2] Executing Data Cleaning Pipeline...")
    duplicate_count = raw_df.duplicated().sum()
    df = raw_df.drop_duplicates().copy()
    print(f"  - Removed {duplicate_count} duplicate rows.")

    df['Shopping Date'] = pd.to_datetime(df['Shopping Date'], errors='coerce')

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    product_price_map = df.groupby('Product Name')['Price'].transform('median')
    df['Price'] = df['Price'].fillna(product_price_map)
    category_price_map = df.groupby('Product Category')['Price'].transform('median')
    df['Price'] = df['Price'].fillna(category_price_map).fillna(999.0)

    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).astype(int)
    df.loc[df['Quantity'] < 1, 'Quantity'] = 1

    df['Customer Age'] = pd.to_numeric(df['Customer Age'], errors='coerce').fillna(30).astype(int)

    # 2.4 Verify & Recalculate Total Amount (Quantity * Price)
    df['Total Amount'] = (df['Quantity'] * df['Price']).round(2)
    df = df.dropna(subset=['Shopping Date', 'Product Category', 'Customer ID']).copy()

    # Feature Engineering
    age_bins = [17, 25, 35, 50, 100]
    age_labels = ['18-25 (Young Adult)', '26-35 (Millennial)', '36-50 (Gen X)', '51+ (Senior)']
    df['Age Group'] = pd.cut(df['Customer Age'], bins=age_bins, labels=age_labels, right=True)
    df['Year-Month'] = df['Shopping Date'].dt.to_period('M').astype(str)

    # 3. High-Level KPI Calculations
    total_revenue = df['Total Amount'].sum()
    total_orders = len(df)
    unique_customers = df['Customer ID'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_units_sold = df['Quantity'].sum()

    print("\n" + "=" * 70)
    print(" EXECUTIVE KPI SUMMARY (INR - ₹)")
    print("=" * 70)
    print(f" Total Revenue:        ₹{total_revenue:,.2f}")
    print(f" Total Orders:         {total_orders:,}")
    print(f" Unique Customers:     {unique_customers:,}")
    print(f" Average Order Value:  ₹{avg_order_value:,.2f}")
    print(f" Total Units Sold:     {total_units_sold:,}")
    print("=" * 70)

    # 4. Detailed Analyses
    category_summary = df.groupby('Product Category').agg(
        Total_Revenue=('Total Amount', 'sum'),
        Order_Count=('Customer ID', 'count'),
        Total_Units=('Quantity', 'sum')
    ).sort_values(by='Total_Revenue', ascending=False)

    print("\n[4.1] Performance by Product Category:")
    print(category_summary.to_string())

    gender_summary = df.groupby('Gender').agg(
        Total_Revenue=('Total Amount', 'sum'),
        Order_Count=('Customer ID', 'count'),
        Avg_Order_Value=('Total Amount', 'mean')
    ).sort_values(by='Total_Revenue', ascending=False)

    print("\n[4.2] Sales by Gender:")
    print(gender_summary.to_string())

    age_summary = df.groupby('Age Group', observed=False).agg(
        Total_Revenue=('Total Amount', 'sum'),
        Order_Count=('Customer ID', 'count')
    )

    payment_summary = df['Payment Method'].value_counts()
    print("\n[4.3] Preferred Payment Methods (Order Volume):")
    for method, count in payment_summary.items():
        pct = (count / total_orders) * 100
        print(f"  - {method:<18}: {count} orders ({pct:.1f}%)")

    city_summary = df.groupby('City')['Total Amount'].sum().sort_values(ascending=False)
    print("\n[4.4] Top Indian Cities by Sales Revenue:")
    for city, rev in city_summary.head(8).items():
        print(f"  - {city:<14}: ₹{rev:,.2f}")

    monthly_trend = df.groupby('Year-Month')['Total Amount'].sum().reset_index()

    top_10_products = df.groupby('Product Name').agg(
        Total_Revenue=('Total Amount', 'sum'),
        Units_Sold=('Quantity', 'sum')
    ).sort_values(by='Total_Revenue', ascending=False).head(10)

    # 5. Visualizations via Matplotlib and Seaborn
    print("\n[5] Generating Visualizations...")

    # Chart 1: Category Sales
    plt.figure(figsize=(10, 5))
    cat_plot = sns.barplot(x=category_summary['Total_Revenue'], y=category_summary.index, palette="Blues_r")
    plt.title("Total Sales Revenue by Product Category (INR ₹)", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Sales Revenue (₹)")
    plt.ylabel("Category")
    for p in cat_plot.patches:
        width = p.get_width()
        cat_plot.annotate(f"₹{width:,.0f}", (width, p.get_y() + p.get_height() / 2.),
                          ha='left', va='center', xytext=(6, 0), textcoords='offset points', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_charts_dir, 'category_sales.png'), dpi=200)
    plt.close()

    # Chart 2: Payment Methods
    plt.figure(figsize=(7, 7))
    plt.pie(payment_summary.values, labels=payment_summary.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette("Set2")[0:len(payment_summary)], wedgeprops=dict(width=0.6, edgecolor='white'))
    plt.title("Payment Methods Distribution (UPI / Cards / COD)", fontsize=13, weight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_charts_dir, 'payment_methods.png'), dpi=200)
    plt.close()

    # Chart 3: Monthly Trend
    plt.figure(figsize=(11, 5))
    plt.plot(monthly_trend['Year-Month'], monthly_trend['Total Amount'], marker='o', linewidth=2.5, color='#2563EB')
    plt.title("Monthly Sales Trend in INR (₹)", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_charts_dir, 'monthly_sales_trend.png'), dpi=200)
    plt.close()

    # Chart 4: Gender Sales
    plt.figure(figsize=(8, 5))
    sns.barplot(x=gender_summary.index, y=gender_summary['Total_Revenue'], palette=["#3B82F6", "#EC4899", "#8B5CF6"])
    plt.title("Total Sales Revenue by Customer Gender (₹)", fontsize=13, weight='bold', pad=12)
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_charts_dir, 'gender_sales.png'), dpi=200)
    plt.close()

    # Chart 5: Age Group
    plt.figure(figsize=(9, 5))
    sns.barplot(x=age_summary.index, y=age_summary['Total_Revenue'], palette="crest")
    plt.title("Purchasing Volume by Customer Age Demographics (₹)", fontsize=13, weight='bold', pad=12)
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_charts_dir, 'age_group_analysis.png'), dpi=200)
    plt.close()

    # Chart 6: Top 10 Products
    plt.figure(figsize=(10, 6))
    top_plot = sns.barplot(x=top_10_products['Total_Revenue'], y=top_10_products.index, palette="viridis")
    plt.title("Top 10 Performing Products by Sales (INR ₹)", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Total Sales Revenue (₹)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_charts_dir, 'top_10_products.png'), dpi=200)
    plt.close()

    print(f"\n✓ All charts generated and saved successfully to: {output_charts_dir}")
    print("=" * 70)

if __name__ == '__main__':
    run_analysis('data.csv')
