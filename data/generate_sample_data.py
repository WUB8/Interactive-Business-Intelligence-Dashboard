import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample online retail data
n_records = 5000

# Generate dates
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_records)]

# Generate invoice numbers
invoice_nos = [f'INV{100000 + i}' for i in range(n_records)]

# Product catalog
products = {
    'Electronics': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'USB Cable', 'Webcam'],
    'Home & Garden': ['Plant Pot', 'Garden Tools', 'Cushion', 'Lamp', 'Picture Frame', 'Vase'],
    'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers', 'Hat', 'Scarf'],
    'Books': ['Fiction Book', 'Non-Fiction Book', 'Magazine', 'Comic Book', 'Textbook'],
    'Toys': ['Board Game', 'Puzzle', 'Action Figure', 'Doll', 'Building Blocks']
}

# Generate stock codes and descriptions
stock_codes = []
descriptions = []
categories = []
for _ in range(n_records):
    category = np.random.choice(list(products.keys()))
    product = np.random.choice(products[category])
    categories.append(category)
    descriptions.append(product)
    stock_code = f'{category[:3].upper()}{np.random.randint(1000, 9999)}'
    stock_codes.append(stock_code)

# Generate quantities (most orders 1-10 items, some larger)
quantities = np.random.choice([1, 2, 3, 4, 5, 6, 10, 12, 20, 24], n_records, p=[0.3, 0.2, 0.15, 0.1, 0.08, 0.07, 0.05, 0.03, 0.01, 0.01])

# Generate unit prices based on category
price_ranges = {
    'Electronics': (15, 800),
    'Home & Garden': (5, 150),
    'Clothing': (10, 200),
    'Books': (8, 50),
    'Toys': (10, 80)
}

unit_prices = []
for category in categories:
    min_price, max_price = price_ranges[category]
    price = round(np.random.uniform(min_price, max_price), 2)
    unit_prices.append(price)

# Generate customer IDs (some customers buy multiple times)
customer_ids = np.random.choice(range(10000, 10500), n_records)

# Generate countries (mostly UK, some international)
countries = np.random.choice(
    ['United Kingdom', 'Germany', 'France', 'Spain', 'Netherlands', 'Belgium', 'Switzerland', 'USA', 'Australia'],
    n_records,
    p=[0.7, 0.08, 0.07, 0.05, 0.04, 0.02, 0.02, 0.01, 0.01]
)

# Add some cancelled orders (negative quantities)
cancel_indices = np.random.choice(range(n_records), size=int(n_records * 0.02), replace=False)
quantities_with_cancels = quantities.copy()
quantities_with_cancels[cancel_indices] *= -1

# Create DataFrame
df = pd.DataFrame({
    'InvoiceNo': invoice_nos,
    'StockCode': stock_codes,
    'Description': descriptions,
    'Quantity': quantities_with_cancels,
    'InvoiceDate': dates,
    'UnitPrice': unit_prices,
    'CustomerID': customer_ids,
    'Country': countries,
    'Category': categories
})

# Add some missing values to make it realistic
missing_indices = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
df.loc[missing_indices, 'CustomerID'] = np.nan

# Sort by date
df = df.sort_values('InvoiceDate').reset_index(drop=True)

# Save to CSV
df.to_csv('online_retail.csv', index=False)
print(f"Generated {len(df)} records")
print(f"Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
print(f"Categories: {df['Category'].unique()}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nDataset info:")
print(df.info())
