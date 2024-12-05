from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome(keep_alive=False)


def extract_price(price_str):
    price_cleaned = re.findall(r'\d+[.,]?\d*', price_str)
    if price_cleaned:
        return float(price_cleaned[0].replace(',', '.'))
    return None


database_products = []

for i in range(1, 5):
    if i != 1:
        url = f'https://vkusvill.ru/offers/?PAGEN_1={i}'
    else:
        url = 'https://vkusvill.ru/offers/'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(2)
    products = soup.find_all(
        class_='ProductCard__link rtext _desktop-md _mobile-sm gray900 js-datalayer-catalog-list-name')
    new_prices = soup.find_all(class_='Price Price--md Price--gray Price--label')
    old_prices = soup.find_all(class_='js-datalayer-catalog-list-price-old hidden')
    # discount_type = soup.find_all(class_='ProductCard__notice')
    if not products:
        break
    for product, old_price, new_price in zip(products, old_prices, new_prices):
        database_products.append((product.get_text().strip().replace('\xa0', ' '),
                                  extract_price(old_price.get_text().strip()),
                                  extract_price(new_price.get_text().strip().replace('\u2009₽', ' '))))

driver.quit()

