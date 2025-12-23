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
    driver.execute_script("arguments[0].scrollIntoView(true);", anchor)
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

        time.sleep(2)
        driver.execute_script("arguments[0].click();", any_clsfc) # closed dropdown    

        print(f"\nSuccessfully navigated to: {driver.current_url}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def view_indiv_jobs(driver):
    try:
        ...
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

# keep browser open
def main():
    driver = add_chrome_driver()
    driver.get("https://ph.jobstreet.com")
    wait = WebDriverWait(driver, 10) # an explicit wait

    seek_swe_listings(driver, wait)
    
    # view_indiv_jobs(driver)
    wait.until(EC.any_of(
            EC.presence_of_element_located((By.XPATH, "//a[@data-automation='job-list-view-job-link']"))   
        )
    )

    # jobs return only the page-loaded jobs
    jobs = driver.find_elements(By.XPATH, "//article[@data-automation='normalJob']")
    counter = 0
    print(len(jobs))
    for job in jobs:
        if counter == 2:
            break
        try:
            driver.execute_script("arguments[0].click();", job) # chore: don't open job in a new tab
            counter += 1
            print(f"Succesful click! Counter: {counter}")
            time.sleep(3)
        except Exception as e:
            print(f"Unsuccesful click: {e}")

    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    main()