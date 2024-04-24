import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd
import traceback

import typing as T

# Custom Exemption
class DataMissingError(Exception):
    """
        If the data is not there we will raise this exemption
    """
    pass

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

time.sleep(3)

all_matches_button = driver.find_element(by=By.XPATH, value=all_matches_xpath)
all_matches_button.click()

# change the Selector button

WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.ID, "country"))
)

dropdown_country = driver.find_element(By.ID, "country")
select_country = Select(dropdown_country)

try:
    select_country.select_by_value("USA")
except:
    print("select_by_value not working")
    traceback.print_exc()
    try:
        select_country.select_by_visible_text("USA")
    except:
        print("select_by_visible_text not working")
        traceback.print_exc()

time.sleep(5)
WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@data-ng-if="!vm.isLoading"]'))
)
# After clicking the `All Match Buton` find the row and extract the data

matches = driver.find_elements(by=By.TAG_NAME, value="tr")

final_data = []
for match in matches:
    columns = match.find_elements(by=By.TAG_NAME, value="td")
    try:
        temp = {
            "date": columns[0].text,
            "home_team": columns[1].text,
            "score": columns[2].text,
            "opposite_tema": columns[3].text
        }
    except:
        traceback.print_exc()
        continue

    final_data.append(temp)

if not final_data:
    raise DataMissingError("Data missing 404")

def create_file(data:T.List[T.Dict], is_csv:bool=None, is_json:bool=None)->None:
    """
        This File create a `excel`, `csv`, `.json` file based on the requirements.
        Default's its create as a `excel file`
        Args:
            `data (List[Dict])` : The data arguments recieve the list of dict
            `is_csv (Boolean)` : To Create a file as `.csv` file.
            `is_json (Boolean)` : To Create a `.json` file.
    """
    df = pd.DataFrame(data)

    file_name = "./temp/app_selenium"

    if not is_csv and not is_json:
        file_name += ".xlsx"
        df.to_excel(file_name, index=False)
        return
    
    if is_csv:
        file_name += ".csv"
        df.to_csv(file_name)
        return

    if is_json:
        file_name += ".json"
        df.to_json(file_name)
        return

create_file(final_data)

time.sleep(5)