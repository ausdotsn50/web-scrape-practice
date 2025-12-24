from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import time, traceback, pprint

# Global
counter = 0
job_ad_details = []

# chrome driver
def add_chrome_driver():
    return webdriver.Chrome()

def add_explicit_wait(driver):
    return WebDriverWait(driver, 10) # an explicit wait

def anchor_click(driver, wait, xpath):
    anchor = wait.until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
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

        wait.until(
            EC.visibility_of_element_located((By.ID, "classificationsPanel"))
        )
        time.sleep(3) # anchor sleep
        
        #anchor_click(driver, wait, "//a[@data-automation='6281']")
        #anchor_click(driver, wait, "//a[@data-automation='6290']")
        
        #anchor_click(driver, "//a[@data-automation='6281']")
        #anchor_click(driver, "//a[@data-automation='6284']")
        
        anchor_click(driver, wait, "//a[@data-automation='6246']")

        # Click seek button
        seek = driver.find_element(By.XPATH, "//button[@data-automation='searchButton']")
        driver.execute_script("arguments[0].click();", seek)
        time.sleep(5) # find a more robust solution[]
        driver.execute_script("arguments[0].click();", any_clsfc) # closed dropdown    

        print(f"\nSuccessfully navigated to: {driver.current_url}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def view_indiv_jobs(driver, wait, curr_counter):
    wait.until(EC.any_of(
            EC.presence_of_element_located((By.XPATH, "//a[@data-automation='job-list-view-job-link']"))   
        )
    )

    # jobs return only the page-loaded jobs
    jobs = driver.find_elements(By.XPATH, "//article[@data-automation='normalJob']")
    for job in jobs:
        """
        if curr_counter == 5:
            break
        """
        try:
            driver.execute_script("arguments[0].click();", job)
            curr_counter += 1
            print(f"Succesful click! Counter: {curr_counter}")
            # time.sleep(3) # job extraction sleep
            jad_container = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-automation='jobAdDetails']"))
            )
            job_ad_details.append({"text": jad_container.text})
            
        except Exception as e:
            print(f"Unsuccesful click: {e}")

# keep browser open
def main():
    driver = add_chrome_driver()
    driver.get("https://ph.jobstreet.com")
    wait = add_explicit_wait(driver)
    pp = pprint.PrettyPrinter(indent=4) # pp printer obj
    counter = 0
    seek_swe_listings(driver, wait)
    
    while True:
        view_indiv_jobs(driver, wait, counter)
        try:
            ref_to_next = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Next']"))
            )
            hdn_status = ref_to_next.get_attribute("aria-hidden")
            print(hdn_status)
            if hdn_status == "false":
                driver.execute_script("arguments[0].click();", ref_to_next)
                print("Next button clicked")
            else:
                print("Next button is hidden. Breaking out of loop.")
                break
        except Exception as e:
            print(e)
            traceback.print_exc()
            break
    
    # pp.pprint(job_ad_details)
    print(len(job_ad_details))

    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    main()