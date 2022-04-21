from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\\Users\\Hp EliteBook\\Desktop\\chrome Driver\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
import lxml

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36 ",
    "Accept-Language": "en-US,en;q=0.9"
}
GOOGLE_form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSdo7zu5LRpUJNE7eAMgN0qOS07CL2uVXTtCesFF_3ieRDtEjA/viewform' \
                   '?usp=sf_link '
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-126.750955953125%2C%22east%22%3A-118.115702046875%2C%22south%22%3A35.18482646968213%2C%22north%22%3A40.27807601439276%7D%2C%22mapZoom%22%3A7%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
response = requests.get(zillow_link, headers=HEADER)
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
soup.prettify()
time.sleep(3)
# ------------------------------------------list of house price--------------------------------------------
house_price_list = [price.get_text().split('/')[0] for price in soup.find_all("div", class_="list-card-price")]
print(house_price_list)
# --------------------------------list of house address---------------------------------------
house_address = [address.text for address in soup.select('.list-card-addr')]
print(house_address)
# ----------------------------------list of links of  each house--------------------------

all_link_elements = soup.select(".list-card-top a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
print(all_links)

# ------------------------------send to spreadsheet----------------------------------
for n in range(len(all_links)):
    driver.get(GOOGLE_form_link)

    time.sleep(2)
    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(house_address[n])
    price.send_keys(house_price_list[n])
    link.send_keys(all_links[n])
    submit_button.click()