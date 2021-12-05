import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time

chrome_driver_path = r"C:\Users\Samet\AppData\Local\Programs\Python\Python310\chromedriver.exe"
ser = Service(chrome_driver_path)

BROWSER_HEADER = {
    "Accept-Language": "en-US",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

response = requests.get("https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22"
                        "pagination%22%3A%7B%7D%2C%22"
                        "usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22"
                        "east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22"
                        "north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filter"
                        "State%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22"
                        "value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22"
                        "value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22"
                        "value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22"
                        "value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22"
                        "max%22%3A3000%7D%2C%22"
                        "price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22"
                        "isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D", headers=BROWSER_HEADER)


response_text = response.text
soup = BeautifulSoup(response_text, "lxml")
print(soup.text)

prices = soup.find_all("div", class_="list-card-price")
price_list = [price.text[:6] for price in prices]
print(price_list)

house_links = soup.find_all("a", class_="list-card-link")
house_list = []
for house in house_links[0::2]:
    if house.get('href')[:5] != "https":
        total_link = "https://www.zillow.com" + house.get('href')
        house_list.append(total_link)
    else:
        house_list.append(house.get('href'))
print(house_list)

addresses = soup.find_all("address", class_="list-card-addr")
address_list = [address.text for address in addresses]
print(address_list)

driver = webdriver.Chrome(service=ser)
counter = 0

while counter < len(house_list):

    driver.get("https://forms.gle/9SAKhxyACFq8k8KA8")
    time.sleep(3)
    text_areas = driver.find_elements(By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
    text_areas[0].send_keys(address_list[counter])
    text_areas[1].send_keys(price_list[counter])
    text_areas[2].send_keys(house_list[counter])
    time.sleep(1)
    press_send = driver.find_element(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel")
    press_send.click()
    time.sleep(2)
    counter += 1



