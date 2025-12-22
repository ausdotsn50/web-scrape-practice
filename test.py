from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import time

# chrome driver
driver = webdriver.Chrome()
driver.get("https://ph.jobstreet.com")

try:
    wait = WebDriverWait(driver, 10)
    
    # open dropdown using JS
    any_clsfc = wait.until(
        EC.presence_of_element_located((By.XPATH, "//label[@data-automation='classificationDropDownListBackdrop']"))
    )
    
    # sol to: ElementNotInteractableException
    driver.execute_script("arguments[0].click();", any_clsfc) # opened dropdown    
    time.sleep(1.5)
    
    any_clsfc_panel = wait.until(
        EC.visibility_of_element_located((By.ID, "classificationsPanel"))
    )

    # Do a scroll to view method
    # Status: scroll ft. applied
    ict_anchor = driver.find_element(By.XPATH, "//a[@data-automation='6281']")
    driver.execute_script("arguments[0].scrollIntoView(true);", ict_anchor) # opened dropdown   
    time.sleep(2)

    driver.execute_script("arguments[0].click();", ict_anchor)

    swe_anchor = driver.find_element(By.XPATH, "//a[@data-automation='6290']")
    driver.execute_script("arguments[0].scrollIntoView(true);", swe_anchor) # opened dropdown   
    time.sleep(2)

    driver.execute_script("arguments[0].click();", swe_anchor)
    
    # Click seek button
    seek = driver.find_element(By.XPATH, "//button[@data-automation='searchButton']")
    driver.execute_script("arguments[0].click();", seek)

    print(f"\n✓ Successfully navigated to: {driver.current_url}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# keep browser open
input("Press Enter to close browser...")
driver.quit()