import time

from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By

from ScrapedData import *

#Inicialize the driver
driver = webdriver.Firefox()  
driver.maximize_window()  
driver.get('https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&disposition=DISP_2_KK&disposition=DISP_2_1&disposition=DISP_3_KK&disposition=DISP_3_1&priceTo=15000&surfaceFrom=40&regionOsmIds=R438344&osm_value=Plze%C5%88%2C+okres+Plze%C5%88-m%C4%9Bsto%2C+Plze%C5%88sk%C3%BD+kraj%2C+Jihoz%C3%A1pad%2C+%C4%8Cesko#lat=49.74172501797827&lng=13.371914800000013&zoom=11.95907496555022')
#Wait for cookies
time.sleep(2)
#Define function to click on cookie
def cookieClicker():
    driver.find_element(By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
    return 0
cookie_not_clicked = 1
#Clicks to accept cookies
while cookie_not_clicked:
    try:
        cookieClicker()
        cookie_not_clicked = 0
    except:
        print('Page was not ready, wating 0.3 sec')
        time.sleep(0.3)

articles_xpath = '/html/body/div[3]/main/section/div/div[2]/div/div[5]/section'
articles_box = driver.find_elements(By.XPATH, articles_xpath)
articles = articles_box[0].find_elements(By.XPATH, 'article')

author_name_xpath = 'div[2]/h2/a/span[2]'
flat_size_rooms_xpath = 'div[2]/ul/li[1]'
flat_size_m_xpath = 'div[2]/ul/li[2]'
extra_info_xpath = 'div[2]/p'
price_xpath = 'div[2]/div/span[1]'
extra_price_xpath = 'div[2]/div/span[2]'
link_xpath = 'div[2]/h2/a'
scraped_data = ScrapedDataHolder()

def extract_data(articles, author_name_xpath, flat_size_rooms_xpath, flat_size_m_xpath, price_xpath, extra_price_xpath, link_xpath, scraped_data):
    for article in articles:
        scraped_data.fulltext.append(article.text)
        author_city_czech_part = article.find_element(By.XPATH, author_name_xpath).text.rsplit(',')
        scraped_data.flat_size_rooms.append(article.find_element(By.XPATH, flat_size_rooms_xpath).text)
        scraped_data.flat_size_m.append(article.find_element(By.XPATH, flat_size_m_xpath).text)
        scraped_data.address.append(author_city_czech_part[0]) 
        scraped_data.city.append(author_city_czech_part[1])
        scraped_data.czech_part.append(author_city_czech_part[2])
        scraped_data.price.append(article.find_element(By.XPATH, price_xpath).text)
        scraped_data.link.append(article.find_element(By.XPATH, link_xpath).get_attribute('href'))
        try:
            scraped_data.extra_price.append(article.find_element(By.XPATH, extra_price_xpath).text)
        except NoSuchElementException:
            scraped_data.extra_price.append('Not specified')
    return scraped_data

scraped_data = extract_data(articles, author_name_xpath, flat_size_rooms_xpath, flat_size_m_xpath, price_xpath, extra_price_xpath, link_xpath, scraped_data)
next_page_xpath = 'html/body/div[3]/main/section/div/div[2]/div/div[5]/section/ul/li[3]/a'
try:
    while True:
        driver.execute_script("window.scrollTo(0, 10000)")
        time.sleep(0.5)
        driver.find_element(By.XPATH, next_page_xpath).click()
        print('New page found')
        time.sleep(3)
        articles_box = driver.find_elements(By.XPATH, articles_xpath)
        articles = articles_box[0].find_elements(By.XPATH, 'article')
        scraped_data = extract_data(articles, author_name_xpath, flat_size_rooms_xpath, flat_size_m_xpath, price_xpath, extra_price_xpath, link_xpath, scraped_data)
except NoSuchElementException:
    print('Last page reached, no clickable button found')
except ElementNotInteractableException:
    print('Last page reached, no clickable button found')
print('Reading complete')
print('Opening a file results.csv')
writer = ScreadDataWriter(scraped_data)
writer.saveData('New_data.xlsx')
print('Closing a fil results.csv')