import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('myntra_300_products.csv')
print(f"Original data shape: {df.shape}")

# Remove duplicates
df = df.drop_duplicates()
print(f"After removing duplicates: {df.shape}")

# Handle missing values - convert various formats to NaN
print("Checking for missing values...")
missing_values = ['', ' ', 'null', 'NULL', 'None', 'N/A', 'n/a', '-', '--', 'nan', 'NaN']

# Check what unique values exist before cleaning
print("Sample unique values in each column:")
for col in df.columns:
    unique_vals = df[col].unique()[:5]  # Show first 5 unique values
    print(f"{col}: {unique_vals}")

df = df.replace(missing_values, np.nan)

# Also check for whitespace-only entries
df = df.applymap(lambda x: np.nan if isinstance(x, str) and x.strip() == '' else x)

# Convert MRP to numeric (handle currency symbols)
if 'MRP' in df.columns:
    df['MRP'] = df['MRP'].astype(str).str.replace('[₹$,]', '', regex=True)
    df['MRP'] = pd.to_numeric(df['MRP'], errors='coerce')

# Convert Discounted Price to numeric (handle currency symbols)
if 'Discounted Price' in df.columns:
    df['Discounted Price'] = df['Discounted Price'].astype(str).str.replace('[₹$,]', '', regex=True)
    df['Discounted Price'] = pd.to_numeric(df['Discounted Price'], errors='coerce')

# Convert Rating to numeric - handle empty spaces specifically
if 'Rating' in df.columns:
    print(f"Rating column before cleaning: {df['Rating'].unique()[:10]}")
    # First convert to string, strip whitespace, then replace empty with NaN
    df['Rating'] = df['Rating'].astype(str).str.strip()
    df['Rating'] = df['Rating'].replace('', np.nan)
    df['Rating'] = df['Rating'].replace('nan', np.nan)  # Handle string 'nan'
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    print(f"Rating column after cleaning: {df['Rating'].unique()[:10]}")
    print(f"NaN count in Rating: {df['Rating'].isna().sum()}")

# Convert Number of Reviews to numeric
if 'Number of Reviews' in df.columns:
    df['Number of Reviews'] = pd.to_numeric(df['Number of Reviews'], errors='coerce')

# Standardize brand names
if 'Brand' in df.columns:
    # Common brand standardizations
    brand_mapping = {
        'Nike Inc.': 'Nike',
        'Adidas AG': 'Adidas', 
        'H&M Hennes & Mauritz': 'H&M',
        'Levi Strauss & Co.': 'Levis'
    }
    df['Brand'] = df['Brand'].replace(brand_mapping)
    df['Brand'] = df['Brand'].str.strip().str.title()  # Clean whitespace and standardize case

# Drop rows where essential columns are missing
essential_cols = ['Product Name', 'Brand', 'MRP']
df = df.dropna(subset=essential_cols, how='any')

# Save cleaned data
try:
    df.to_csv('cleaned_data.csv', index=False)
    print("✓ Saved to cleaned_data.csv")
except PermissionError:
    # If file is open, try alternative name
    df.to_csv('cleaned_ecommerce_data.csv', index=False)
    print("✓ Saved to cleaned_ecommerce_data.csv")

print(f"\nCleaned data shape: {df.shape}")
print(f"Missing values per column:")
print(df.isnull().sum())
print(f"\nFirst few rows:")
print(df.head())