from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from random import randint
import smtplib, ssl

def load_more():
    try:
        button = driver.find_element("xpath", '//div[@class="ULvh-button show-more-button"]')
        button.click()
        print("Waiting for items to load")
        sleep(randint(25,35))
    except:
        pass

driver = webdriver.Firefox()
sleep(2)
kayak_url = "https://www.kayak.com/flights/LAX-SGN/2023-08-01/2023-08-31/5adults?sort=bestflight_a"
driver.get(kayak_url)

sleep(15)

load_more()
flight_rows = driver.find_elements("xpath", '//div[@class="nrc6"]')

prices = []
company = []
for web_element in flight_rows:
    element_HTML = web_element.get_attribute('outerHTML')
    bs = BeautifulSoup(element_HTML, 'html.parser')

    temp = bs.find("div", {"class": "nrc6-price-section"})
    price = temp.find("div", {"class": "f8F1-price-text"})

    prices.append(price.text)
    
    company_name = bs.find("div", {"class": "J0g6-operator-text"})

    if company_name == None:
        company_name = bs.find("div", {"class": "c_cgF c_cgF-mod-variant-default"})
        
    company.append(company_name.text)

result = []

for i in range(len(prices)):
    result.append((prices[i], company[i]))
print(result)

message = ""


def send_email(message):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "EMAIL"  # Enter your address
    receiver_email = "EMAIL"  # Enter receiver address
    password = "PASSWORD"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)