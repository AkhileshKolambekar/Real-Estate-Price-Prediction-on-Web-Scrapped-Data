from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time 

import pandas as pd
import numpy as np

options = webdriver.ChromeOptions()
options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )

browser = webdriver.Chrome(options=options) #define the browser
browser.get('https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Pune')

#For BHK and Property
dic = {
    'Property':[],
    'Bhk':[],
    'Floor':[],
    'Area':[],
    'Price':[]
}

last_height = browser.execute_script("return document.body.scrollHeight") #Store height of the page at that point

BHKTargetCount = 3000 #Till how many elements it must be scrolled

st = time.time()
page = 0

while BHKTargetCount>len(dic['Bhk']):
    page = page+1
    print("Scrolling",page,len(dic['Bhk']))
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);") #Scroll the page till the end
    time.sleep(30) #Allow the page to load
    new_height = browser.execute_script("return document.body.scrollHeight") #Get the height of the page
    if new_height == last_height:
        break
    last_height = new_height #Update the height

    elements = browser.find_elements(By.CLASS_NAME,"mb-srp__list")
    for element in elements:
        property_type = element.find_element(By.CLASS_NAME,"mb-srp__card--title").text.split()[2]
        dic['Property'].append(property_type)

        bhk = element.find_element(By.CLASS_NAME,"mb-srp__card--title").text.split()[0]
        dic['Bhk'].append(bhk)

        price = element.find_element(By.CLASS_NAME,"mb-srp__card__price--amount").text
        dic['Price'].append(price)

        try:
            floor = element.find_element(By.CSS_SELECTOR,'div[data-summary="floor"]').text.split()[1]
            dic['Floor'].append(floor)
        except:
            dic['Floor'].append(np.NaN)

        try:
            area = element.find_element(By.CSS_SELECTOR,'div[data-summary="carpet-area"]').text.split()[2]
            dic['Area'].append(area)
        except:
            dic['Area'].append(np.NaN)

print('Scrolling Finished')
print(time.time()-st)

data = pd.DataFrame(dic)
data.to_csv('data.csv',index=False)