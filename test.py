from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://ph.jobstreet.com")

try:
    wait = WebDriverWait(driver, 10)
    
    # Step 1: Enter keywords
    keyword_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Enter keywords']"))
    )
    keyword_input.send_keys("software developer")
    print("✓ Entered keywords")
    
    """
    # Step 2: Find and click the classification dropdown (try multiple selectors)
    # Try different ways to locate the dropdown
    classification_dropdown = None
    selectors = [
        (By.XPATH, "//button[contains(@aria-label, 'classification')]"),
        (By.XPATH, "//input[@aria-label='Job classifications']"),
        (By.CSS_SELECTOR, "input[data-automation='job-classifications']"),
        (By.XPATH, "//div[contains(text(), 'Any classification')]"),
        (By.CSS_SELECTOR, "button[aria-expanded='false']"),
    ]
    
    for selector_type, selector_value in selectors:
        try:
            classification_dropdown = wait.until(
                EC.element_to_be_clickable((selector_type, selector_value))
            )
            print(f"✓ Found dropdown using: {selector_value}")
            break
        except:
            continue
    
    if not classification_dropdown:
        print("✗ Could not find classification dropdown, skipping...")
    else:
        classification_dropdown.click()
        time.sleep(1.5)
        print("✓ Opened classification dropdown")
        
        # Click on "Information & Communication Technology"
        try:
            ict_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Information & Communication Technology')]"))
            )
            ict_option.click()
            time.sleep(0.5)
            print("✓ Selected ICT classification")
            
            # Close dropdown
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except Exception as e:
            print(f"Could not select classification: {e}")
    """
    # Step 3: Enter location
    location_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter suburb, city, or region']")
    location_input.send_keys("Cebu")
    print("✓ Entered location")
    
    # Step 4: Click search
    search_button = driver.find_element(By.XPATH, "//button[@data-automation='searchButton']")
    search_button.click()
    print("✓ Clicked search button")
    
    # Wait for results
    time.sleep(3)
    
    print(f"\n✓ Successfully navigated to: {driver.current_url}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Chrome quit
input("Press Enter to close...")
driver.quit()