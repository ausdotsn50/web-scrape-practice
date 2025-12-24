from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, traceback, pprint


# Global
job_ad_details = []


def add_chrome_driver():
   return webdriver.Chrome()


def add_explicit_wait(driver):
   return WebDriverWait(driver, 10)


def anchor_click(driver, wait, xpath):
   anchor = wait.until(
       EC.presence_of_element_located((By.XPATH, xpath))
   )
   driver.execute_script("arguments[0].scrollIntoView(true);", anchor)
   driver.execute_script("arguments[0].click();", anchor)
  
def seek_swe_listings(driver, wait):
   try:   
       any_clsfc = wait.until(
           EC.presence_of_element_located((By.XPATH, "//label[@data-automation='classificationDropDownListBackdrop']"))
       )
      
       driver.execute_script("arguments[0].click();", any_clsfc)


       wait.until(
           EC.visibility_of_element_located((By.ID, "classificationsPanel"))
       )
       time.sleep(2)
      
       anchor_click(driver, wait, "//a[@data-automation='6246']")


       seek = driver.find_element(By.XPATH, "//button[@data-automation='searchButton']")
       driver.execute_script("arguments[0].click();", seek)
       time.sleep(3)


       print(f"\n✓ Successfully navigated to: {driver.current_url}")
   except Exception as e:
       print(f"✗ Error: {e}")
       traceback.print_exc()


def wait_for_job_details_to_stabilize(driver, wait):
   """Wait for job details to fully load"""
   try:
       jad_container = wait.until(
           EC.presence_of_element_located((By.XPATH, "//div[@data-automation='jobAdDetails']"))
       )
      
       # Wait for content to stabilize
       previous_length = 0
       stable_count = 0
      
       for _ in range(10):
           try:
               # Re-fetch element to avoid stale reference
               jad_container = driver.find_element(By.XPATH, "//div[@data-automation='jobAdDetails']")
               current_text = jad_container.text
               current_length = len(current_text)
              
               if current_length == previous_length and current_length > 100:
                   stable_count += 1
                   if stable_count >= 2:
                       return jad_container
               else:
                   stable_count = 0
              
               previous_length = current_length
               time.sleep(0.3)
           except:
               time.sleep(0.3)
               continue
      
       return jad_container
   except:
       return None


def view_indiv_jobs(driver, wait):
   """
   Process all jobs on the current page
   Returns the number of jobs processed
   """
   # Wait for job list to be present
   wait.until(
       EC.presence_of_element_located((By.XPATH, "//article[@data-automation='normalJob']"))
   )
  
   # Small delay for page to stabilize
   time.sleep(1)
  
   processed = 0
   job_index = 0
   max_attempts = 50  # Safety limit
  
   while job_index < max_attempts:
       try:
           # Re-find all jobs on each iteration
           jobs = driver.find_elements(By.XPATH, "//article[@data-automation='normalJob']")
          
           if job_index >= len(jobs):
               print(f"\n✓ Processed all {len(jobs)} jobs on this page")
               break
          
           job = jobs[job_index]
          
           # Check if this job is already selected (has active/selected class)
           try:
               is_selected = driver.execute_script("""
                   let job = arguments[0];
                   // Check if job has selected/active class or attribute
                   return job.classList.contains('selected') ||
                          job.classList.contains('active') ||
                          job.getAttribute('aria-current') === 'true' ||
                          job.querySelector('a[aria-current="true"]') !== null;
               """, job)
              
               if is_selected:
                   print(f"  [SKIP] Job {job_index + 1} is already selected, capturing details...")
                  
                   # Just capture the details without clicking
                   jad_container = wait_for_job_details_to_stabilize(driver, wait)
                  
                   if jad_container:
                       job_text = jad_container.text
                       job_url = driver.current_url
                      
                       job_ad_details.append({
                           "job_number": len(job_ad_details) + 1,
                           "text": job_text,
                           "url": job_url,
                           "length": len(job_text)
                       })
                      
                       print(f"    ✓ Captured {len(job_text)} characters (pre-selected)")
                  
                   processed += 1
                   job_index += 1
                   continue
                  
           except Exception as e:
               print(f"  Warning: Could not check selection status: {e}")
          
           # Scroll into view
           driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job)
           time.sleep(0.5)
          
           # Click the job
           try:
               driver.execute_script("arguments[0].click();", job)
               processed += 1
              
               print(f"  [{processed}] Clicked job {job_index + 1}/{len(jobs)}")
              
               # Wait for URL to change (job details loaded)
               time.sleep(1.5)
              
               # Wait for job details to fully load
               jad_container = wait_for_job_details_to_stabilize(driver, wait)
              
               if jad_container:
                   job_text = jad_container.text
                   job_url = driver.current_url
                  
                   job_ad_details.append({
                       "job_number": len(job_ad_details) + 1,
                       "text": job_text,
                       "url": job_url,
                       "length": len(job_text)
                   })
                  
                   print(f"    ✓ Captured {len(job_text)} characters")
               else:
                   print(f"    ⚠ Failed to load job details")
              
           except Exception as click_error:
               print(f"    ✗ Error clicking: {click_error}")
               # Try to continue anyway
          
           # Move to next job
           job_index += 1
          
           # Small delay before next job
           time.sleep(0.5)
          
       except Exception as e:
           print(f"  ✗ Error processing job {job_index + 1}: {e}")
           # Try to continue with next job
           job_index += 1
           time.sleep(0.5)
           continue
  
   return processed


def main():
   driver = add_chrome_driver()
   driver.get("https://ph.jobstreet.com")
   wait = add_explicit_wait(driver)
  
   seek_swe_listings(driver, wait)
  
   page_number = 1
  
   while True:
       print(f"\n{'='*50}")
       print(f"Processing Page {page_number}")
       print(f"{'='*50}")
      
       processed = view_indiv_jobs(driver, wait)
      
       print(f"\n✓ Processed {processed} jobs on page {page_number}")
       print(f"✓ Total jobs scraped so far: {len(job_ad_details)}")
      
       # Check for Next button
       try:
           # Scroll to top to ensure Next button is accessible
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(1)
          
           ref_to_next = wait.until(
               EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Next']"))
           )
           hdn_status = ref_to_next.get_attribute("aria-hidden")
          
           print(f"\nNext button aria-hidden: {hdn_status}")
          
           if hdn_status == "false":
               # Scroll to next button
               driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ref_to_next)
               time.sleep(0.5)
              
               # Click next
               driver.execute_script("arguments[0].click();", ref_to_next)
               print(f"✓ Clicked 'Next' button")
              
               # CRITICAL: Wait for new page to load
               time.sleep(3)
              
               # Wait for new job list to appear
               wait.until(
                   EC.presence_of_element_located((By.XPATH, "//article[@data-automation='normalJob']"))
               )
               time.sleep(1)
              
               page_number += 1
           else:
               print("\n✓ Reached last page")
               break
              
       except Exception as e:
           print(f"\n✗ Error with pagination: {e}")
           traceback.print_exc()
           break
  
   print(f"\n{'='*50}")
   print(f"SCRAPING COMPLETE")
   print(f"{'='*50}")
   print(f"Total pages processed: {page_number}")
   print(f"Total jobs scraped: {len(job_ad_details)}")
  
   if job_ad_details:
       print(f"\nFirst job preview:")
       print(f"  URL: {job_ad_details[0]['url']}")
       print(f"  Length: {job_ad_details[0]['length']} characters")
       print(f"  Preview: {job_ad_details[0]['text'][:200]}...")
  
   input("\nPress Enter to close browser...")
   driver.quit()


if __name__ == "__main__":
   main()
