import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample data for testing
np.random.seed(42)

# Generate sample sales data
n_records = 500

data = {
    'Date': [datetime.now() - timedelta(days=x) for x in range(n_records)],
    'Product': np.random.choice(['Laptop', 'Desktop', 'Tablet', 'Smartphone', 'Monitor'], n_records),
    'Category': np.random.choice(['Electronics', 'Accessories'], n_records),
    'Sales_Amount': np.random.uniform(500, 5000, n_records),
    'Quantity': np.random.randint(1, 50, n_records),
    'Customer_ID': np.random.randint(1000, 9999, n_records),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
    'Discount_Percent': np.random.uniform(0, 30, n_records),
}

# Create DataFrame
df = pd.DataFrame(data)

# Introduce some missing values (10% of data)
missing_indices = np.random.choice(len(df), size=int(len(df)*0.1), replace=False)
df.loc[missing_indices[:len(missing_indices)//2], 'Discount_Percent'] = np.nan
df.loc[missing_indices[len(missing_indices)//2:], 'Sales_Amount'] = np.nan

# Introduce some duplicates
df = pd.concat([df, df.iloc[:20]], ignore_index=True)

# Round values
df['Sales_Amount'] = df['Sales_Amount'].round(2)
df['Discount_Percent'] = df['Discount_Percent'].round(2)

# Save to Excel
df.to_excel('sample_data.xlsx', index=False, engine='openpyxl')

print("✅ Sample Excel file created: sample_data.xlsx")
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")
