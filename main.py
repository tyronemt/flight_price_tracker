from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
sleep(2)
kayak_url = "https://www.kayak.com/flights/LAX-SGN/2023-08-01/2023-08-31/5adults?sort=bestflight_a"
driver.get(kayak_url)

sleep(15)
flight_rows = driver.find_elements("xpath", '//div[@class="nrc6"]')

print(flight_rows)

prices = []
company = []
for web_element in flight_rows:
    element_HTML = web_element.get_attribute('outerHTML')
    bs = BeautifulSoup(element_HTML, 'html.parser')

    temp = bs.find("div", {"class": "nrc6-price-section"})
    price = temp.find("div", {"class": "f8F1-price-text"})

    prices.append(price.text)
   
    # company_names = bs.findAll("div", {"class": "c_cgF c_cgF-mod-variant-default"})
    # print(company_names.text)

print(prices)