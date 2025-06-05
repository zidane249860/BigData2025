from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Launching browser...")

# Set up driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

print("Opening Google...")
driver.get("https://www.google.com")

# Keep the browser open for 10 seconds
time.sleep(10)

driver.quit()
print("Browser closed.")
