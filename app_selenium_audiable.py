import os
import traceback
import pandas as pd
import typing as T

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

final_data = []
for card in audio_cards:
    temp = {
        "image_url": card.find_element(By.CSS_SELECTOR, "picture > img").get_attribute("src")
    }

    final_data.append(temp)


def create_file(data:T.List[T.Dict], is_json:bool=None)->None:
    """
        This function is used to create file using the scraped data

        Args:
            data (list[dict]) : The data contains the list of dict with scraped data
            is_json (bool) : To create a file as a `.json` format file
    """

    # Create a data frame
    df = pd.DataFrame(data)

    file_name = "./temp/app_selenium_audiable"
    if is_json:
        df.to_json(file_name+".json")
    else:
        df.to_excel(file_name+".xlsx", index=False)

create_file(final_data)