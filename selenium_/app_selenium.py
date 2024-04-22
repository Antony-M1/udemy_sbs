from selenium import webdriver


website = "https://www.adamchoi.co.uk/overs/detailed"

# Chrome Driver Path

driver_path = "../ch_driver/chromedriver"

driver = webdriver.Chrome(driver_path)

driver.get(website)