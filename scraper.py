from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# Helper function to extract price from text like "₹599"
def get_price(text):
    if text:
        numbers = re.findall(r'\d+', text.replace(',', ''))
        if numbers:
            return int(numbers[0])
    return None

# Helper function to extract rating
def get_rating(text):
    if text:
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            return float(numbers[0])
    return None

print("🛍️ Starting Myntra scraper for 300 products...")
print("This will take a few minutes...")

# Step 1: Open browser
driver = webdriver.Chrome()
driver.get("https://www.myntra.com/men-tshirts")
time.sleep(5)

# Step 2: Set up variables
all_products = []
minimum_target = 300  # AT LEAST 300 products
page = 1

print(f" Target: AT LEAST {minimum_target} products")

# Step 3: Loop through pages until we get AT LEAST 300 products
while len(all_products) < minimum_target:
    print(f"\nPAGE {page} - Products collected: {len(all_products)}")
    
    # Wait for products to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-base"))
        )
    except:
        time.sleep(3)
    
    # Get all products on current page
    products = driver.find_elements(By.CSS_SELECTOR, ".product-base")
    print(f"Found {len(products)} products on this page")
    
    if not products:
        print("No products found. Stopping.")
        break
    
    # Step 4: Extract data from each product
    for i, product in enumerate(products):
        # Continue collecting even after minimum target to finish the page
        try:
            # Scroll to product
            driver.execute_script("arguments[0].scrollIntoView(true);", product)
            time.sleep(0.3)
            
            # 1. Product Name
            try:
                product_name = product.find_element(By.CSS_SELECTOR, ".product-product").text
            except:
                product_name = "Not Available"
            
            # 2. Brand
            try:
                brand = product.find_element(By.CSS_SELECTOR, ".product-brand").text
            except:
                brand = "Not Available"
            
            # Skip if no name or brand
            if product_name == "Not Available" or brand == "Not Available":
                continue
            
            # 3. Category
            category = "Men's T-Shirts"
            
            # 4. Discounted Price
            try:
                price_element = product.find_element(By.CSS_SELECTOR, ".product-discountedPrice")
                discounted_price = get_price(price_element.text)
            except:
                discounted_price = None
            
            # 5. MRP
            try:
                mrp_element = product.find_element(By.CSS_SELECTOR, ".product-strike")
                mrp = get_price(mrp_element.text)
            except:
                mrp = discounted_price
            
            # 6. Rating
            try:
                rating_element = product.find_element(By.CSS_SELECTOR, ".product-ratingsContainer")
                rating = get_rating(rating_element.text)
            except:
                rating = None
            
            # 7. Number of Reviews
            try:
                review_element = product.find_element(By.CSS_SELECTOR, ".product-ratingsCount")
                review_text = review_element.text
                if 'k' in review_text.lower():
                    num = float(re.findall(r'\d+\.?\d*', review_text)[0])
                    number_of_reviews = int(num * 1000)
                else:
                    numbers = re.findall(r'\d+', review_text)
                    number_of_reviews = int(numbers[0]) if numbers else 0
            except:
                number_of_reviews = 0
            
            # 8. Product URL
            try:
                link_element = product.find_element(By.CSS_SELECTOR, "a")
                product_url = link_element.get_attribute("href")
            except:
                product_url = "Not Available"
            
            # Save product data
            product_data = {
                'Product Name': product_name,
                'Brand': brand,
                'Category': category,
                'MRP': mrp,
                'Discounted Price': discounted_price,
                'Rating': rating,
                'Number of Reviews': number_of_reviews,
                'Product URL': product_url
            }
            
            all_products.append(product_data)
            
            # Only print progress every 50 products
            if len(all_products) % 50 == 0:
                print(f"Progress: {len(all_products)} products collected...")
            
        except Exception as e:
            # Don't print individual errors, just count them
            continue
    
    # Step 5: Go to next page if we haven't reached minimum
    if len(all_products) < minimum_target:
        try:
            # Find next button
            next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-next")
            
            # Check if next button is disabled
            if "pagination-disabled" in next_button.get_attribute("class"):
                print(" No more pages available!")
                break
            
            # Click next page
            driver.execute_script("arguments[0].click();", next_button)
            page += 1
            time.sleep(3)  # Wait for page to load
            
        except Exception as e:
            print(f" Can't go to next page: {e}")
            break
    else:
        print(f" Reached minimum target! Got {len(all_products)} products!")
        # Continue to finish current page but don't go to next page
        break

# Step 6: Close browser
driver.quit()
print("Browser closed")

# Step 7: Save all data
if all_products:
    df = pd.DataFrame(all_products)
    filename = "myntra_300_products.csv"
    df.to_csv(filename, index=False)
    
    print(f"\n SUCCESS!")
    print(f" Total products collected: {len(all_products)}")
    print(f"Saved to: {filename}")
    
    