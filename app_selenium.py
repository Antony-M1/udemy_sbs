import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd


# Create `temp` folder is its not there
temp_dir_path = "./temp"

if not os.path.exists(temp_dir_path):
    os.mkdir(temp_dir_path)
    print("Temp Folder Created")

website = "https://www.adamchoi.co.uk/overs/detailed"

# Chrome Driver Path

driver_path = "./chromedriver.exe"

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)


driver.get(website)

all_matches_xpath = '//label[@analytics-event="All matches"]'

# Wait for the element to get load
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, all_matches_xpath))
) # After 5 Sec the element we can't able find the element means crash the program or go head for next move

all_matches_button = driver.find_element(by=By.XPATH, value=all_matches_xpath)
all_matches_button.click()

# After clicking the `All Match Buton` find the row and extract the data

matches = driver.find_elements(by=By.TAG_NAME, value="tr")

final_data = []
for match in matches:
    columns = match.find_elements(by=By.TAG_NAME, value="td")
    temp = {
        "date":columns[0].text,
        "home_team": columns[1].text,
        "score": columns[2].text,
        "opposite_tema": columns[3].text
    }
    final_data.append(temp)

time.sleep(10)