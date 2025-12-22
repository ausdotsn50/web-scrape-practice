from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import time, traceback

# chrome driver
def add_chrome_driver():
    return webdriver.Chrome()

def anchor_click(driver, xpath):
    anchor = driver.find_element(By.XPATH, xpath)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", anchor)
    
def seek_swe_listings(driver, wait):
    try:    
        # open dropdown using JS
        any_clsfc = wait.until(
            EC.presence_of_element_located((By.XPATH, "//label[@data-automation='classificationDropDownListBackdrop']"))
        )
        
        # sol to: ElementNotInteractableException
        driver.execute_script("arguments[0].click();", any_clsfc) # opened dropdown    
        
        anchor_click(driver, "//a[@data-automation='6281']")
        anchor_click(driver, "//a[@data-automation='6290']")
        
        # Click seek button
        seek = driver.find_element(By.XPATH, "//button[@data-automation='searchButton']")
        driver.execute_script("arguments[0].click();", seek)

        print(f"\nSuccessfully navigated to: {driver.current_url}")
    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()

# keep browser open
def main():
    driver = add_chrome_driver()
    driver.get("https://ph.jobstreet.com")
    wait = WebDriverWait(driver, 10) # an explicit wait

    seek_swe_listings(driver, wait)

    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    main()