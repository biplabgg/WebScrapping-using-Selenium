from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# **Set Chrome Options with Custom User-Agent**
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
chrome_options.add_argument("--headless")  # Run in headless mode (remove if debugging)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# **Initialize WebDriver with Options**
 # Change path if needed
driver = webdriver.Chrome(options=chrome_options)

# **Open Apartments.com with a search query**
search_url = "https://www.apartments.com/new-york-ny/"
driver.get(search_url)

# **Wait for elements to load**
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "placardContainer")))

# **Scroll down multiple times to load more listings**
for _ in range(5):  # Adjust for more listings
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)  # Give time for new listings to load

# **Extract apartment listings**
apartments = driver.find_elements(By.CLASS_NAME, "placard")

apartment_data = []
for apt in apartments:
    try:
        name = apt.find_element(By.CLASS_NAME, "property-title").text.strip()
        price = apt.find_element(By.CLASS_NAME, "property-pricing").text.strip()
        address = apt.find_element(By.CLASS_NAME, "property-address").text.strip()
        link = apt.find_element(By.TAG_NAME, "a").get_attribute("href")

        apartment_data.append({
            "Name": name,
            "Price": price,
            "Address": address,
            "Link": link
        })
    except:
        continue  # Skip if any data is missing

# **Save data to CSV**
df = pd.DataFrame(apartment_data)
df.to_csv("apartments.csv", index=False)
# **Close the browser**
driver.quit()

print("Scraping completed! Data saved to 'apartments.csv'.")
