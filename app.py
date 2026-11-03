"""
Customer Shopping Analysis - Interactive Streamlit Dashboard (Indian Retail Edition)
Technologies: Streamlit, Pandas, NumPy, Plotly, Altair, Matplotlib
Currency: Indian Rupee (INR ₹)
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Customer Shopping Analysis - Indian Retail",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for clean professional aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading & Cleaning Function
@st.cache_data
def load_and_clean_data(file_path="data.csv"):
    if not os.path.exists(file_path):
        alt_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            return None, {"error": "data.csv not found"}

    raw_df = pd.read_csv(file_path)
    initial_count = len(raw_df)

    # 1. Remove duplicate records
    dup_count = int(raw_df.duplicated().sum())
    df = raw_df.drop_duplicates().copy()

    # 2. Correct Data Types & Parse Dates
    df['Shopping Date'] = pd.to_datetime(df['Shopping Date'], errors='coerce')

    # 3. Handle Missing Values and Invalids
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    product_price_map = df.groupby('Product Name')['Price'].transform('median')
    df['Price'] = df['Price'].fillna(product_price_map)
    category_price_map = df.groupby('Product Category')['Price'].transform('median')
    df['Price'] = df['Price'].fillna(category_price_map).fillna(999.0)

    # Quantity cleaning
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).astype(int)
    df.loc[df['Quantity'] < 1, 'Quantity'] = 1

    # Age cleaning
    df['Customer Age'] = pd.to_numeric(df['Customer Age'], errors='coerce').fillna(30).astype(int)

    # 4. Calculate / Re-verify Total Sales (Total Amount = Quantity * Price in INR ₹)
    df['Total Amount'] = (df['Quantity'] * df['Price']).round(2)

    df = df.dropna(subset=['Shopping Date', 'Product Category', 'Customer ID']).copy()

    # Feature Engineering
    age_bins = [17, 25, 35, 50, 100]
    age_labels = ['18-25', '26-35', '36-50', '51+']
    df['Age Group'] = pd.cut(df['Customer Age'], bins=age_bins, labels=age_labels, right=True)
    df['Month_Year'] = df['Shopping Date'].dt.strftime('%Y-%m')
    df['Month_Name'] = df['Shopping Date'].dt.strftime('%b %Y')

    cleaning_stats = {
        "initial_rows": initial_count,
        "cleaned_rows": len(df),
        "duplicates_removed": dup_count,
        "cleanliness_rate": round((len(df) / initial_count) * 100, 1)
    }

    return df, cleaning_stats

df, stats = load_and_clean_data("data.csv")

if df is None:
    st.error("Error: 'data.csv' was not found. Please run 'python generate_data.py' to generate the dataset.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filters")

min_date = df['Shopping Date'].min().date()
max_date = df['Shopping Date'].max().date()

date_range = st.sidebar.date_input(
    "Select Shopping Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

gender_options = ["All"] + sorted(list(df['Gender'].dropna().unique()))
selected_gender = st.sidebar.selectbox("Customer Gender", options=gender_options, index=0)

all_cities = sorted(list(df['City'].dropna().unique()))
selected_cities = st.sidebar.multiselect(
    "Filter by Indian City",
    options=all_cities,
    default=all_cities
)

all_categories = sorted(list(df['Product Category'].dropna().unique()))
selected_categories = st.sidebar.multiselect(
    "Product Categories",
    options=all_categories,
    default=all_categories
)

# Apply filters
filtered_df = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = filtered_df[
        (filtered_df['Shopping Date'].dt.date >= start_d) &
        (filtered_df['Shopping Date'].dt.date <= end_d)
    ]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_cities:
    filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

if selected_categories:
    filtered_df = filtered_df[filtered_df['Product Category'].isin(selected_categories)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Orders:** `{len(filtered_df):,}` / `{len(df):,}`")
st.sidebar.markdown(f"**Duplicates Cleaned:** `{stats['duplicates_removed']}`")
st.sidebar.caption("Currency: Indian Rupee (₹)")

# 4. Main Dashboard Header
st.markdown('<div class="main-header">Customer Shopping Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Indian retail market analysis: purchasing behavior, category revenues in INR (₹), customer demographics, and payment trends.</div>',
    unsafe_allow_html=True
)

if len(filtered_df) == 0:
    st.warning("No records match the current filter criteria. Please broaden your selection.")
    st.stop()

# 5. Executive KPI Cards
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

total_revenue = filtered_df['Total Amount'].sum()
total_orders = len(filtered_df)
unique_customers = filtered_df['Customer ID'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

with kpi_col1:
    st.metric(
        label="Total Sales Revenue",
        value=f"₹{total_revenue:,.2f}",
        help="Sum of (Quantity × Price) in INR"
    )

with kpi_col2:
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}",
        help="Total number of completed shopping transactions"
    )

with kpi_col3:
    st.metric(
        label="Unique Customers",
        value=f"{unique_customers:,}",
        help="Distinct customer IDs in filtered set"
    )

with kpi_col4:
    st.metric(
        label="Average Order Value (AOV)",
        value=f"₹{avg_order_value:,.2f}",
        help="Mean revenue per transaction in INR"
    )

st.markdown("---")

tab_overview, tab_categories, tab_demographics, tab_trends, tab_data = st.tabs([
    "📊 Executive Overview",
    "🏷️ Category & Products",
    "👥 Demographics & Cities",
    "📈 Monthly Trends & UPI",
    "📋 Raw Data Explorer"
])

# TAB 1: EXECUTIVE OVERVIEW
with tab_overview:
    col_chart_left, col_chart_right = st.columns(2)

    with col_chart_left:
        st.subheader("Category-Wise Sales Revenue (₹)")
        cat_data = filtered_df.groupby('Product Category')['Total Amount'].sum().reset_index()
        cat_data = cat_data.sort_values(by='Total Amount', ascending=True)

        fig_cat = px.bar(
            cat_data,
            x='Total Amount',
            y='Product Category',
            orientation='h',
            text='Total Amount',
            color='Total Amount',
            color_continuous_scale='Blues',
            labels={'Total Amount': 'Revenue (₹)', 'Product Category': 'Category'}
        )
        fig_cat.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_cat.update_layout(height=380, margin=dict(l=10, r=20, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_chart_right:
        st.subheader("Payment Methods Share (UPI, Cards, COD)")
        pay_data = filtered_df.groupby('Payment Method').agg(
            Orders=('Customer ID', 'count'),
            Revenue=('Total Amount', 'sum')
        ).reset_index()

        fig_pay = px.pie(
            pay_data,
            names='Payment Method',
            values='Orders',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_pay.update_traces(textposition='inside', textinfo='percent+label')
        fig_pay.update_layout(height=380, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_pay, use_container_width=True)

    # Monthly Trend (Full Width)
    st.subheader("Monthly Sales Trend (INR ₹)")
    trend_data = filtered_df.groupby('Month_Year')['Total Amount'].sum().reset_index()
    trend_data = trend_data.sort_values(by='Month_Year')

    fig_trend = px.line(
        trend_data,
        x='Month_Year',
        y='Total Amount',
        markers=True,
        labels={'Month_Year': 'Month', 'Total Amount': 'Revenue (₹)'}
    )
    fig_trend.update_traces(line_color='#2563EB', line_width=3, marker_size=7)
    fig_trend.update_layout(height=320, margin=dict(l=10, r=20, t=20, b=10))
    st.plotly_chart(fig_trend, use_container_width=True)

# TAB 2: CATEGORY & PRODUCTS
with tab_categories:
    col_p1, col_p2 = st.columns([3, 2])

    with col_p1:
        st.subheader("Top 10 Products by Total Sales (₹)")
        top_products = filtered_df.groupby('Product Name').agg(
            Revenue=('Total Amount', 'sum'),
            Units_Sold=('Quantity', 'sum')
        ).reset_index().sort_values(by='Revenue', ascending=True).tail(10)

        fig_top = px.bar(
            top_products,
            x='Revenue',
            y='Product Name',
            orientation='h',
            text='Revenue',
            color='Revenue',
            color_continuous_scale='Viridis',
            labels={'Revenue': 'Revenue (₹)', 'Product Name': 'Product'}
        )
        fig_top.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_top.update_layout(height=420, margin=dict(l=10, r=20, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)

    with col_p2:
        st.subheader("Category Performance Metrics")
        cat_metrics = filtered_df.groupby('Product Category').agg(
            Total_Revenue=('Total Amount', 'sum'),
            Total_Orders=('Customer ID', 'count'),
            Avg_Price=('Price', 'mean')
        ).reset_index().sort_values(by='Total_Revenue', ascending=False)

        cat_metrics['Avg_Price'] = cat_metrics['Avg_Price'].round(2)
        cat_metrics['Revenue_Share'] = (cat_metrics['Total_Revenue'] / total_revenue * 100).round(1).astype(str) + '%'
        cat_metrics['Total_Revenue'] = cat_metrics['Total_Revenue'].map('₹{:,.2f}'.format)
        cat_metrics['Avg_Price'] = cat_metrics['Avg_Price'].map('₹{:,.2f}'.format)
        st.dataframe(cat_metrics, use_container_width=True, hide_index=True)

# TAB 3: DEMOGRAPHICS & CITIES
with tab_demographics:
    demo_c1, demo_c2 = st.columns(2)

    with demo_c1:
        st.subheader("Gender-Wise Shopping Revenue & Volume")
        gender_data = filtered_df.groupby('Gender').agg(
            Revenue=('Total Amount', 'sum'),
            Orders=('Customer ID', 'count')
        ).reset_index()

        fig_gender = px.bar(
            gender_data,
            x='Gender',
            y='Revenue',
            color='Gender',
            text='Revenue',
            color_discrete_map={'Male': '#3B82F6', 'Female': '#EC4899', 'Other': '#8B5CF6'},
            labels={'Revenue': 'Revenue (₹)'}
        )
        fig_gender.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_gender.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_gender, use_container_width=True)

    with demo_c2:
        st.subheader("Age Group Distribution")
        age_data = filtered_df.groupby('Age Group', observed=False).agg(
            Revenue=('Total Amount', 'sum'),
            Orders=('Customer ID', 'count')
        ).reset_index()

        fig_age = px.bar(
            age_data,
            x='Age Group',
            y='Revenue',
            color='Age Group',
            text='Revenue',
            color_discrete_sequence=px.colors.sequential.Teal,
            labels={'Revenue': 'Revenue (₹)'}
        )
        fig_age.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_age.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)

    # City Breakdown
    st.subheader("Top Indian Cities by Sales Volume & Revenue")
    city_data = filtered_df.groupby('City')['Total Amount'].sum().reset_index().sort_values(by='Total Amount', ascending=False)
    fig_city = px.bar(
        city_data,
        x='City',
        y='Total Amount',
        color='Total Amount',
        text='Total Amount',
        color_continuous_scale='Purples',
        labels={'Total Amount': 'Revenue (₹)'}
    )
    fig_city.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig_city.update_layout(height=340, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
    st.plotly_chart(fig_city, use_container_width=True)

# TAB 4: MONTHLY TRENDS & UPI
with tab_trends:
    trend_c1, trend_c2 = st.columns(2)

    with trend_c1:
        st.subheader("Payment Method Usage Across Categories")
        pay_cat = pd.crosstab(filtered_df['Product Category'], filtered_df['Payment Method'])
        fig_pay_cat = px.bar(
            pay_cat,
            barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pay_cat.update_layout(height=400, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_pay_cat, use_container_width=True)

    with trend_c2:
        st.subheader("Average Order Value (AOV) by City")
        city_aov = filtered_df.groupby('City').agg(
            AOV=('Total Amount', 'mean'),
            Orders=('Customer ID', 'count')
        ).reset_index().sort_values(by='AOV', ascending=False)
        
        fig_city_aov = px.bar(
            city_aov,
            x='City',
            y='AOV',
            text='AOV',
            color='AOV',
            color_continuous_scale='Viridis',
            labels={'AOV': 'AOV (₹)'}
        )
        fig_city_aov.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_city_aov.update_layout(height=400, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_city_aov, use_container_width=True)

# TAB 5: RAW DATA EXPLORER
with tab_data:
    st.subheader("Indian Retail Transaction Records")
    st.write(f"Showing **{len(filtered_df):,}** records in INR (₹).")

    search_query = st.text_input("Search (Customer ID, Product, City, Category):", "")
    display_df = filtered_df.copy()
    if search_query:
        mask = (
            display_df['Customer ID'].astype(str).str.contains(search_query, case=False) |
            display_df['Product Name'].astype(str).str.contains(search_query, case=False) |
            display_df['City'].astype(str).str.contains(search_query, case=False) |
            display_df['Product Category'].astype(str).str.contains(search_query, case=False)
        )
        display_df = display_df[mask]

    st.dataframe(
        display_df.sort_values(by='Shopping Date', ascending=False),
        use_container_width=True,
        hide_index=True
    )

    csv_bytes = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_bytes,
        file_name="indian_customer_shopping_data.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Customer Shopping Analysis Dashboard | Indian Retail Edition | Streamlit & Pandas")
