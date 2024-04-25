import os
import traceback
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Create a temp folder
temp_dir_path = "./temp"
if not os.path.exists(temp_dir_path):
    os.mkdir(temp_dir_path)
    print("temp folder created")


web_uri = "https://www.audible.in/adblbestsellers" # Best seller Page

# Initialise the Driver
driver_exe_path = "./chromedriver.exe"
service = Service(driver_exe_path)
driver = webdriver.Chrome(service=service)

# Load the Page
driver.get(web_uri)

# Waiting for the right element to load
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'li.productListItem'))
) # This funtion is wait for the element to get load


# get all the cards
audio_cards = driver.find_elements(By.CSS_SELECTOR, "li.productListItem")

for card in audio_cards:
    print(card)