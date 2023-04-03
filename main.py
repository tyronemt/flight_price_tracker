from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from random import randint
import smtplib, ssl
import numpy as np
import pandas


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
    print("Send Email")

def load_more():
    try:
        print("Loading more Data")
        button = driver.find_element("xpath", '//div[@class="ULvh-button show-more-button"]')
        button.click()
        print("Waiting for items to load")
        sleep(randint(25,35))
    except:
        pass

def manipulate_data(data):
    sum = 0
    num = 0
    for i in range(len(data)):
        price = data[i][0].replace(',', '')
        price = price.replace('$', '')
        price = int(price)
        data[i] = list(data[i])
        data[i][0] = price
        data[i] = tuple(data[i])
        sum += price
        num += 1
    average = sum // num
    data.sort()
    cheapest = data[0][0]
    city = data[0][1]

    message = "the average price for a ticket is ${average}.\nThe cheapest price for a ticket is ${cheapest} {city}.\n\n".format(average = average, cheapest = cheapest, city = city)
    message += "Data:  {data}".format(data = data)
    return message


airport1 = 'LAX'
airport2 = 'SGN'
date1 = '2023-08-01'
date2 = '2023-08-31'


driver = webdriver.Firefox()
sleep(2)
kayak_url = "https://www.kayak.com/flights/{airport1}-{airport2}/{date1}/{date2}?sort=bestflight_a".format(airport1 = airport1, airport2 = airport2, date1 = date1, date2 = date2)
driver.get(kayak_url)

sleep(15)

for i in range(25):
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

m = manipulate_data(result)


message = "Out of {num} data points, ".format(num = len(result)) + m

send_email(message)


