# Customer Shopping Analysis

Customer Shopping Analysis is a data analytics and dashboard project focused on Indian retail purchasing behavior. It cleans raw shopping transaction data, computes business KPIs, performs exploratory analysis, and presents the results in an interactive dashboard built with Streamlit.

## Project Overview
This project analyzes a synthetic but realistic Indian retail dataset containing more than 1,350 customer transactions across major Indian cities. The analysis covers customer demographics, product categories, payment trends, city-wise sales, and monthly revenue performance.

The project is designed to show how raw customer data can be transformed into useful business insights using Python, Pandas, and data visualization libraries.

## Objectives
- Build a clean and realistic retail dataset for analysis.
- Detect and remove duplicate or invalid transaction records.
- Validate numeric fields such as quantity, price, and age.
- Calculate business KPIs such as revenue, orders, and average order value.
- Compare sales across categories, payment methods, cities, and customer segments.
- Present the findings in an interactive dashboard for business users.
- Create a portfolio-ready project suitable for interviews and resume showcasing.

## Dataset Description
The dataset is a synthetic retail sales dataset modeled around Indian shopping behavior.

- Total records: 1,350+
- Cities covered: 12 major Indian cities
- Categories: Electronics, Clothing & Fashion, Home & Kitchen, Beauty & Personal Care, Sports & Fitness, Books & Stationery
- Payment methods: UPI, Credit Card, Debit Card, Net Banking, Cash on Delivery
- Fields include: Customer ID, Customer Age, Gender, Product Category, Product Name, Quantity, Price, Total Amount, Payment Method, Shopping Date, and City

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

## Project Workflow
1. Generate the sales dataset using `generate_data.py`.
2. Clean and validate the dataset using `analysis.py`.
3. Produce charts and summary outputs in the `charts/` folder.
4. Explore the results in the interactive Streamlit dashboard via `app.py`.

## Project Structure
```text
customer-shopping-analysis/
├── app.py                # Streamlit dashboard for retail analytics
├── analysis.py           # Data cleaning, KPI computation, and chart generation
├── charts/               # Generated output visualizations
├── data.csv              # Customer shopping dataset
├── generate_data.py      # Dataset generation script
├── requirements.txt      # Required Python packages
├── .gitignore            # Files to exclude from GitHub upload
├── README.md             # Project documentation
└── venv/                 # Local virtual environment (ignored by Git)
```

## Installation Instructions
1. Open the project folder in VS Code or any code editor.
2. Create a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run the Project
### Run the data analysis script
```bash
python analysis.py
```
This script cleans the data, calculates key metrics, and saves charts in the `charts/` directory.

### Launch the Streamlit dashboard
```bash
streamlit run app.py
```
Then open the local URL shown in the terminal, typically:
```text
http://localhost:8501
```

## Screenshots of the Output
The following charts are generated as part of the analysis and are saved in the `charts/` folder:

![Category Sales](charts/category_sales.png)

![Payment Methods](charts/payment_methods.png)

![Monthly Sales Trend](charts/monthly_sales_trend.png)

![Gender Revenue](charts/gender_sales.png)

![Age Group Analysis](charts/age_group_analysis.png)

![Top Products](charts/top_10_products.png)

## Key Insights and Results
After running the analysis, the project identified the following important outcomes:

- Total Revenue: ₹4,390,080.00
- Total Orders: 1,350
- Unique Customers: 549
- Average Order Value: ₹3,251.91
- Top payment method: UPI with 43.9% of transactions
- Top categories by revenue: Electronics, Clothing & Fashion, Home & Kitchen
- Top-performing cities: Chennai, Ahmedabad, Jaipur, Hyderabad

These insights help businesses understand customer purchase behavior and prioritize revenue-driving segments.

## Summary
This project demonstrates end-to-end data analytics in a practical retail scenario. It combines data cleaning, business intelligence, and dashboard building in one portfolio-ready application.

It is suitable for students, beginners, and job seekers who want to showcase data analysis skills in interviews and on GitHub.

## License
This project is intended for educational and portfolio use.
