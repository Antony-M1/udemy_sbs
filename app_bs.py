import requests
import traceback
from bs4 import BeautifulSoup


website = "https://subslikescript.com/movie/Titanic-120338"

try:
    result = requests.get(website)
except requests.exceptions.ConnectionError:
    raise requests.exceptions.ConnectionError("🌐🌐 Please Check the Network")


content = result.text

soup = BeautifulSoup(content, 'lxml')

box = soup.find("article", class_='main-article')

title = box.find("h1").get_text()
full_script = box.find("div", class_="full-script").get_text(strip=True, separator=" ") # Strip Parameter delete the spacese front and back from the string
full_script = box.find("div", class_="full-script").get_text(strip=True, separator="\n") # Strip Parameter delete the spacese front and back from the string


with open(f"./temp/{title}.txt", 'w', encoding='utf-8') as file:
    file.write(full_script)
    # file.close()