import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('cleaned_data.csv')
print(f"Dataset shape: {df.shape}")

# 1. DESCRIPTIVE STATISTICS
print("\n" + "="*50)
print("DESCRIPTIVE STATISTICS")
print("="*50)

# Calculate discount percentage
df['Discount_Percent'] = ((df['MRP'] - df['Discounted Price']) / df['MRP'] * 100).round(2)

# Price statistics
print("\nPRICE STATISTICS:")
price_stats = df[['MRP', 'Discounted Price', 'Discount_Percent']].describe()
print(price_stats)

# Rating statistics
print("\nRATING STATISTICS:")
rating_stats = df['Rating'].describe()
print(rating_stats)

# 2. BRAND ANALYSIS
print("\n" + "="*50)
print("BRAND ANALYSIS")
print("="*50)

# Top 5 brands by number of products
top_brands = df['Brand'].value_counts().head()
print("\nTOP 5 BRANDS BY NUMBER OF PRODUCTS:")
print(top_brands)

# Visualize top brands
plt.figure(figsize=(10, 6))
top_brands.plot(kind='bar', color='skyblue')
plt.title('Top 5 Brands by Number of Products')
plt.xlabel('Brand')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. DISCOUNT ANALYSIS
print("\n" + "="*50)
print("DISCOUNT ANALYSIS")
print("="*50)

# Average discount by brand
avg_discount_by_brand = df.groupby('Brand')['Discount_Percent'].mean().sort_values(ascending=False)
print("\nAVERAGE DISCOUNT % BY BRAND:")
print(avg_discount_by_brand.head(10))

# Visualize discount analysis
plt.figure(figsize=(12, 6))
avg_discount_by_brand.head(10).plot(kind='bar', color='lightcoral')
plt.title('Top 10 Brands by Average Discount Percentage')
plt.xlabel('Brand')
plt.ylabel('Average Discount %')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. CATEGORY-SPECIFIC INSIGHTS
print("\n" + "="*50)
print("CATEGORY-SPECIFIC INSIGHTS")
print("="*50)

# Category analysis
category_analysis = df.groupby('Category').agg({
    'MRP': ['mean', 'min', 'max'],
    'Discounted Price': ['mean', 'min', 'max'],
    'Rating': ['mean', 'count'],
    'Discount_Percent': 'mean'
}).round(2)

print("\nCATEGORY ANALYSIS:")
print(category_analysis)

# Price distribution by category
plt.figure(figsize=(12, 8))

# Subplot 1: Price distribution
plt.subplot(2, 2, 1)
df.boxplot(column='Discounted Price', by='Category', ax=plt.gca())
plt.title('Price Distribution by Category')
plt.suptitle('')

# Subplot 2: Rating distribution
plt.subplot(2, 2, 2)
df.boxplot(column='Rating', by='Category', ax=plt.gca())
plt.title('Rating Distribution by Category')
plt.suptitle('')

# Subplot 3: Discount distribution
plt.subplot(2, 2, 3)
df.boxplot(column='Discount_Percent', by='Category', ax=plt.gca())
plt.title('Discount % Distribution by Category')
plt.suptitle('')

# Subplot 4: Price vs Rating scatter
plt.subplot(2, 2, 4)
plt.scatter(df['Discounted Price'], df['Rating'], alpha=0.6, c='purple')
plt.xlabel('Discounted Price')
plt.ylabel('Rating')
plt.title('Price vs Rating Correlation')

plt.tight_layout()
plt.show()

# 5. ADDITIONAL INSIGHTS
print("\n" + "="*50)
print("ADDITIONAL INSIGHTS")
print("="*50)

# Price-Rating correlation
correlation = df['Discounted Price'].corr(df['Rating'])
print(f"\nPrice-Rating Correlation: {correlation:.3f}")

# Identify anomalies (products with very high discount)
high_discount = df[df['Discount_Percent'] > 70]
print(f"\nProducts with >70% discount: {len(high_discount)}")
if len(high_discount) > 0:
    print("High discount products:")
    print(high_discount[['Product Name', 'Brand', 'MRP', 'Discounted Price', 'Discount_Percent']].head())

# Premium vs Budget products
premium = df[df['Discounted Price'] > df['Discounted Price'].quantile(0.75)]
budget = df[df['Discounted Price'] < df['Discounted Price'].quantile(0.25)]

print(f"\nPremium products (top 25%): Avg Rating = {premium['Rating'].mean():.2f}")
print(f"Budget products (bottom 25%): Avg Rating = {budget['Rating'].mean():.2f}")

# Summary
print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print(f"Total products analyzed: {len(df)}")
print(f"Average discount across all products: {df['Discount_Percent'].mean():.1f}%")
print(f"Average rating: {df['Rating'].mean():.2f}/5")
print(f"Price range: ₹{df['Discounted Price'].min():.0f} - ₹{df['Discounted Price'].max():.0f}")
print(f"Most common brand: {df['Brand'].mode()[0]}")
print(f"Most common category: {df['Category'].mode()[0]}")