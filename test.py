# Source - https://stackoverflow.com/a
# Posted by Ajeet Verma
# Retrieved 2025-12-21, License - CC BY-SA 4.0

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# interact w/ browser w/o exiting
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service)

driver.get("https://www.chess.com/")

#driver.close()