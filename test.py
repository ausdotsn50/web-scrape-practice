from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import time, traceback, pprint

# Global
job_ad_details = []

# chrome driver
def add_chrome_driver():
    return webdriver.Chrome()

def add_explicit_wait(driver):
    return WebDriverWait(driver, 10) # an explicit wait

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
        
        #anchor_click(driver, "//a[@data-automation='6281']")
        #anchor_click(driver, "//a[@data-automation='6290']")
        
        anchor_click(driver, "//a[@data-automation='6281']")
        anchor_click(driver, "//a[@data-automation='6284']")
        
        # Click seek button
        seek = driver.find_element(By.XPATH, "//button[@data-automation='searchButton']")
        driver.execute_script("arguments[0].click();", seek)

        time.sleep(2)
        driver.execute_script("arguments[0].click();", any_clsfc) # closed dropdown    

        print(f"\nSuccessfully navigated to: {driver.current_url}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def view_indiv_jobs(driver, wait):
    wait.until(EC.any_of(
            EC.presence_of_element_located((By.XPATH, "//a[@data-automation='job-list-view-job-link']"))   
        )
    )

    # jobs return only the page-loaded jobs
    jobs = driver.find_elements(By.XPATH, "//article[@data-automation='normalJob']")
    counter = 0
    for job in jobs:
        """
        if counter == 2:
            break
        """
        try:
            driver.execute_script("arguments[0].click();", job) # chore: don't open job in a new tab
            counter += 1
            print(f"Succesful click! Counter: {counter}")
            time.sleep(5)

            jad_container = driver.find_element(By.XPATH, "//div[@data-automation='jobAdDetails']")
            job_ad_details.append({"text": jad_container.text})

            time.sleep(5)
        except Exception as e:
            print(f"Unsuccesful click: {e}")
    """
    try:
        ...
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    """

# keep browser open
def main():
    driver = add_chrome_driver()
    driver.get("https://ph.jobstreet.com")
    wait = add_explicit_wait(driver)
    pp = pprint.PrettyPrinter(indent=4) # pp printer obj

    seek_swe_listings(driver, wait)
    
    while True:
        view_indiv_jobs(driver, wait)
        try:
            ref_to_next = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
            hdn_status = ref_to_next.get_attribute("aria-hidden")   
        except Exception as e:
            print(e)
            break

        if hdn_status == "false":
            continue
        else: 
            break

    pp.pprint(job_ad_details)
    print(len(job_ad_details))

    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    main()