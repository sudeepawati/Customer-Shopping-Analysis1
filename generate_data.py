"""
Customer Shopping Dataset Generator - Indian Retail Edition
Generates a realistic shopping transactions dataset with at least 1,250 records.
Includes Indian cities, INR (₹) pricing, UPI/Cards/COD payment methods,
and intentional anomalies for data cleaning demonstration.
"""

import os
import random
import csv
from datetime import datetime, timedelta

def generate_indian_shopping_data(num_records=1350, output_file='data.csv'):
    random.seed(42)

    # Categories with realistic Indian retail pricing in INR (₹)
    categories = {
        'Electronics': [
            ('Wireless Noise-Canceling Earbuds', 2999.00),
            ('Smart Fitness Watch V2', 4499.00),
            ('Bluetooth Portable Bass Speaker', 1899.00),
            ('4K Ultra HD Streaming Stick', 3499.00),
            ('Ergonomic Mechanical Keyboard', 3999.00),
            ('Precision Wireless Mouse', 999.00),
            ('Fast Charging 20000mAh Power Bank', 1499.00),
            ('Dual-Port 65W GaN Charger', 1999.00),
            ('Noise-Canceling Over-Ear Headphones', 7999.00)
        ],
        'Clothing & Fashion': [
            ('Slim-Fit Stretch Denim Jeans', 1799.00),
            ('Pure Cotton Solid Crewneck T-Shirt', 699.00),
            ('Ethnic Embroidered Kurta Set', 2499.00),
            ('Formal Wrinkle-Free Office Shirt', 1499.00),
            ('Comfort Fleece Winter Hoodie', 1899.00),
            ('Waterproof Windcheater Jacket', 2299.00),
            ('Handloom Cotton Chino Trousers', 1599.00),
            ('Traditional Silk Blend Festive Saree', 3499.00)
        ],
        'Home & Kitchen': [
            ('Pre-Seasoned Cast Iron Dosa Tawa', 1299.00),
            ('Automatic Espresso & Drip Coffee Machine', 4999.00),
            ('Non-Stick Hard Anodized 3-Piece Cookware', 2899.00),
            ('100% Cotton 300TC Double Bed Sheet Set', 1399.00),
            ('Stainless Steel Insulated Water Bottle 1L', 699.00),
            ('Ceramic Ultrasonic Essential Oil Diffuser', 1199.00),
            ('Multi-Speed Food Mixer Grinder 750W', 3299.00)
        ],
        'Beauty & Personal Care': [
            ('10% Niacinamide Clarifying Face Serum', 599.00),
            ('Ultra-Matte Mineral SPF 50 Gel Sunscreen', 499.00),
            ('Ayurvedic Deep Scalp Conditioning Hair Oil', 449.00),
            ('Vitamin C Radiance Face Moisturizer', 699.00),
            ('Salon Pro Ionic Hair Dryer 2000W', 2199.00),
            ('Organic Green Tea Foaming Face Wash', 349.00)
        ],
        'Sports & Fitness': [
            ('Extra-Dense Anti-Skid Yoga Mat 6mm', 899.00),
            ('Rubber Coated Hex Dumbbell Pair (10kg)', 3499.00),
            ('Engineered Mesh Running Shoes', 2899.00),
            ('Lightweight Badminton Racket with Cover', 1699.00),
            ('Water-Resistant Sports Duffle Gym Bag', 1099.00),
            ('Resistance Loop Bands 5-Piece Exercise Set', 599.00)
        ],
        'Books & Stationery': [
            ('Data Science & Machine Learning with Python', 899.00),
            ('Hardcover Dotted Premium Journal Notebook', 499.00),
            ('Classic Fountain Pen with Ink Cartridges', 799.00),
            ('Financial Freedom & Investing Guide Paperback', 399.00),
            ('Minimalist Daily Productivity Desk Planner', 450.00)
        ]
    }

    # Major Indian Cities & Tech/Shopping Hubs
    cities = [
        'Bengaluru', 'Mumbai', 'Delhi NCR', 'Hyderabad',
        'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur',
        'Kochi', 'Chandigarh', 'Lucknow'
    ]

    # Popular Indian Payment Methods
    payment_methods = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Cash on Delivery']
    genders = ['Male', 'Female', 'Female', 'Male', 'Female', 'Other']

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 3, 31)
    date_range_days = (end_date - start_date).days

    # Customer pool
    num_unique_customers = 620
    customer_pool = []
    for i in range(1, num_unique_customers + 1):
        cust_id = f"IND-CUST-{1000 + i}"
        age = random.choices(
            [random.randint(18, 25), random.randint(26, 35), random.randint(36, 50), random.randint(51, 70)],
            weights=[28, 42, 22, 8]
        )[0]
        gender = random.choice(genders)
        city = random.choice(cities)
        customer_pool.append({
            'id': cust_id,
            'age': age,
            'gender': gender,
            'city': city
        })

    records = []
    category_keys = list(categories.keys())

    for _ in range(num_records):
        cust = random.choice(customer_pool)
        category = random.choices(
            category_keys,
            weights=[25, 23, 18, 15, 11, 8]
        )[0]
        product_name, unit_price = random.choice(categories[category])
        quantity = random.choices([1, 2, 3, 4, 5], weights=[58, 26, 10, 4, 2])[0]
        total_amount = round(quantity * unit_price, 2)
        payment_method = random.choices(
            payment_methods,
            weights=[45, 22, 16, 9, 8]  # UPI is dominant in India
        )[0]

        random_days = random.randint(0, date_range_days)
        shopping_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

        records.append({
            'Customer ID': cust['id'],
            'Customer Age': cust['age'],
            'Gender': cust['gender'],
            'Product Category': category,
            'Product Name': product_name,
            'Quantity': quantity,
            'Price': unit_price,
            'Total Amount': total_amount,
            'Payment Method': payment_method,
            'Shopping Date': shopping_date,
            'City': cust['city']
        })

    # Intentional anomalies for data cleaning demonstration
    # 1. Duplicate records
    for i in range(10):
        records.append(dict(records[i * 25]))

    # 2. Minor anomalies
    records[12]['Total Amount'] = 0.0
    records[35]['Quantity'] = None
    records[70]['Price'] = None

    fieldnames = [
        'Customer ID', 'Customer Age', 'Gender', 'Product Category',
        'Product Name', 'Quantity', 'Price', 'Total Amount',
        'Payment Method', 'Shopping Date', 'City'
    ]

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)

    print(f"Generated {len(records)} Indian retail shopping records saved to '{output_file}'.")
    return output_file

if __name__ == '__main__':
    generate_indian_shopping_data(1350, 'data.csv')
