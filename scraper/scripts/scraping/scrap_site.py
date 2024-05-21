from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup webdriver
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# Open the URL
driver.get('https://ir.amd.com/financial-information')

# Pause for 8 seconds to let the page load and the cookie message to appear
time.sleep(6)

# Find the "Cookies Settings" button and click it
cookies_settings_button = driver.find_element(By.PARTIAL_LINK_TEXT, 'Cookies Settings')
cookies_settings_button.click()

# Pause for 3 seconds to let the cookies settings load
time.sleep(3)

# Wait for the "Confirm My Choices" button to be present and click it
confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="save-preference-btn-handler onetrust-close-btn-handler" and text()="Confirm My Choices"]')))
confirm_button.click()

# Pause for 3 seconds to let the page load
time.sleep(6)

# Wait for the link that contains "Earnings Release" to be clickable and click it



# Wait for the link that contains "Earnings Release" to be clickable and click it
link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Earnings Release")]')))
link.click()
# Pause for 3 seconds to let the page load
time.sleep(3)

# Get the page source
page_source = driver.page_source

# Write the page source to a new HTML file
with open('scraped_page1.html', 'w') as f:
  f.write(page_source)

# Close the driver
driver.quit()