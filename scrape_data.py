import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    timer = time.time()
    print("Scraping")
    url = "https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/?pagination=0&paginationantal=100"
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument("window-size=1920x1480")
    options.add_argument("--headless")
    options.add_argument("disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="114.0.5735.90").install(), options=options)

    driver.get(url)
    time.sleep(30)  # experiment with timer to fetch all the data
    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    data = soup.find("div", {"data-logic": "sok.listor.js"})
    #appartment_titles = data.find_all("h3", {"class": "ObjektTyp"})

    appartments = data.find_all("div", {"class": "media"})
    appartments_dataframe = pd.DataFrame(
        columns=["address", "type", "size", "rent",
                 "personer", "dagar", "time", "url"]
    )
    for appartment in appartments:

        # find address in appartment
        addressdata = appartment.find("h4")
        titledata = appartment.find("h3", {"class": "ObjektTyp"})
        title = titledata.find("a").text
        url = addressdata.find("a").get("href")
        address = addressdata.find("a").text
        appartmentdata = appartment.find(
            "div", {"class": "ObjektDetaljer span6"})
        price = appartmentdata.find("dd", {"class": "ObjektHyra"}).text
        # format price as integer
        price = price.replace("kr", "").strip(" ")

        size = appartmentdata.find("dd", {"class": "ObjektYta"}).text
        # format size string to integer
        size = size.replace("m²", "")
        intresse = appartmentdata.find(
            "dd", {"class": "ObjektAntalIntresse hidden-phone"}
        ).text
        # split intresse in to intresse and antalintresserade
        dagar, personer = intresse.split(" ")
        # remove paranthesis and "st" from personer
        antalintresserade = personer.replace("(", "").replace("st)", "")
        # get today date with hours and minutes
        tid = time.strftime("%Y-%m-%d %H:%M")

        adf = pd.DataFrame.from_records(
            [
                {
                    "address": address,
                    "type": title,
                    "size": (size),
                    "rent": (price),
                    "personer": int(antalintresserade),
                    "dagar": int(dagar),
                    "time": tid,
                    "url": url,
                }
            ]
        )

        # add queuedf datafram as column to adf

        # concatenate the dataframes
        appartments_dataframe = pd.concat([appartments_dataframe, adf])

    # for row in appartments_dataframe add corresponding title to title column

    # close the driver
    driver.close()

    timer = time.time() - timer
    print("Scraping done in", timer, "seconds")
    return appartments_dataframe


if __name__ == "__main__":
    print(scrape())
