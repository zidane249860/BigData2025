from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import pandas as pd
import os

# Data list to hold results
results = []

# Scraping function (modified to store data)
def scrape(current_url):
    scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        company = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "zzDege"))
        ).text

        price = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.YMlKec.fxKbKc"))
        ).text

        timestamp = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ygUjEc[jsname="Vebqub"]'))
        ).text

        print(f"✅ Scraped: {company} | {price} | {timestamp} | {scrape_time}")

        # Store the scraped data
        results.append({
            "Company": company,
            "Price": price,
            "Timestamp": timestamp,
            "URL": current_url,
            "Scraped At": scrape_time
        })

    except Exception as e:
        print("❌ Failed to scrape:", e)
        results.append({
            "Company": "N/A",
            "Price": "N/A",
            "Timestamp": "N/A",
            "URL": current_url,
            "Scraped At": scrape_time
        })

# URLs to scrape
urls = [
    "https://www.google.com/finance/quote/BBCA:IDX?hl=en",
    "https://www.google.com/finance/quote/BMRI:IDX?hl=en",
    "https://www.google.com/finance/quote/BBNI:IDX?hl=en",
    "https://www.google.com/finance/quote/BBRI:IDX?hl=en"
]

# Setup the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the first URL
driver.get(urls[0])
scrape(urls[0])

# Open new tabs and load other URLs
for url in urls[1:]:
    # Open new tab via JS
    driver.execute_script("window.open('');")
    # Switch to the new tab (last in window_handles)
    driver.switch_to.window(driver.window_handles[-1])
    # Load the URL in the new tab
    driver.get(url)
    scrape(url)

# Now all tabs are loaded with their URLs
input("Press Enter to close all tabs...")

driver.quit()

# At the end
df = pd.DataFrame(results)

# Remove duplicate rows based on Company + Timestamp
df.drop_duplicates(subset=["Company", "Timestamp"], inplace=True)

file_path = "stocks.csv"

# Check if file exists
file_exists = os.path.exists(file_path)

# Append if file exists, else write with header
if file_exists:
    df.to_csv(file_path, mode='a' if file_exists else 'w', index=False, encoding='utf-8', header=not file_exists)
    print("📌 Appended to existing stocks.csv")
else:
    df.to_csv(file_path, index=False, encoding="utf-8")
    print("📁 Created new stocks.csv")