import requests
import traceback
import os
from bs4 import BeautifulSoup

# Create a Temp folder
temp_dir = "./temp"

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
    print(f"Directory {temp_dir} created")

root_url = "https://subslikescript.com/"
web_url = f"{root_url}movies" # This url contain all the movies transcript in pangination order

total_links = []
page = 81
while True:
    try:
        main_page = requests.get(f"{web_url}?page={page}")
    except requests.exceptions.ConnectionError:
        raise Exception("Network Issue")
    except:
        break

    main_content = main_page.text

    page_soup = BeautifulSoup(main_content, "lxml")

    main_article = page_soup.find("article", class_="main-article")

    if len(main_article.find_all("a", href=True)) == 0:
        break

    for link in main_article.find_all("a", href=True):
        total_links.append(link['href'])

    for link in total_links:
        try:
            result = requests.get(root_url+link)
            content = result.text
            soup = BeautifulSoup(content, "lxml")

            box = soup.find("article", class_="main-article")
            title = box.find("h1").get_text()
            transcript = box.find("div", class_="full-script").get_text(strip=True, separator="\n")

            if not title:
                c = 1
        except:
            traceback.print_exc()
            continue

        title = title.replace('"', '').replace("?", "").replace("/", "-").replace(":", "").replace("*", "-") # in text file formate these are the files are not allowed
        try:
            with open(f"./temp/{title}.txt", "w", encoding="utf-8") as file:
                file.write(transcript)
        except:
            traceback.print_exc()

    print(f"Page -> {page} & Total Transcripts {len(total_links)}")
    total_links = []
    page += 1

    if page >= 1805:
        print("our condition not working")
        break