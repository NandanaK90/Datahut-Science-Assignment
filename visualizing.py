import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv('cleaned_data.csv')

print(f"Dataset shape: {df.shape}")

# Calculate discount percentage if not exists
if 'Discount_Percent' not in df.columns:
    df['Discount_Percent'] = ((df['MRP'] - df['Discounted Price']) / df['MRP'] * 100).round(2)

# BAR CHART - Average Discount Percentage by Brand
plt.figure(figsize=(12, 8))

# Get top 10 brands by discount percentage
top_brands = df.groupby('Brand')['Discount_Percent'].mean().sort_values(ascending=False).head(10)

# Create bar chart
bars = plt.bar(range(len(top_brands)), top_brands.values, color='lightcoral', alpha=0.8, edgecolor='black')

# Customize chart
plt.title('Average Discount Percentage by Brand (Top 10)', fontsize=16, fontweight='bold')
plt.xlabel('Brand', fontsize=12)
plt.ylabel('Average Discount (%)', fontsize=12)
plt.xticks(range(len(top_brands)), top_brands.index, rotation=45, ha='right')
plt.grid(True, alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, top_brands.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

print("\nBar Chart Summary:")
print("✓ Shows top 10 brands by average discount percentage")
print("✓ Values displayed on each bar")
print("Chart created successfully!")