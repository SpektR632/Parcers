from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()

all_products_from_VV = []  # Можно импортировать в свой файл эту переменную


# from parcer_total_products import all_products_from_VV

def extract_price(price_str):
    price_cleaned = re.findall(r'\d+[.,]?\d*', price_str)
    if price_cleaned:
        return float(price_cleaned[0].replace(',', '.'))
    return None


def parcing(part_of_url):
    for i in range(1, 2):
        if i != 1:
            url = f'https://vkusvill.ru/goods/{part_of_url}?PAGEN_1={i}'
        else:
            url = f'https://vkusvill.ru/goods/{part_of_url}'
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(0.5)
        products = soup.find_all(
            class_='ProductCard__link rtext _desktop-md _mobile-sm gray900 js-datalayer-catalog-list-name')
        descriptions = soup.find_all(class_='Slider__itemInner')
        prices = soup.find_all(class_='js-datalayer-catalog-list-price-old hidden')
        if not products:
            break
        for product, description, price in zip(products, descriptions, prices):
            all_products_from_VV.append((product.get_text().strip().replace('\xa0', ' '),
                                         description.get_text().strip().replace('\xa0', ' ').split('  ')[2],
                                         extract_price(price.get_text().strip())))


categories = ['gotovaya-eda/', 'sladosti-i-deserty/', 'ovoshchi-frukty-yagody-zelen/', 'khleb-i-vypechka/',
              'molochnye-produkty-yaytso/', 'vypekaem-sami/', 'myaso-ptitsa/', 'zamorozhennye-produkty/',
              'kolbasa-sosiski-delikatesy/', 'ryba-ikra-i-moreprodukty/', 'napitki/', 'syry/', 'morozhenoe/'
    , 'supermarket/', 'kafe/', 'orekhi-chipsy-i-sneki/', 'vegetarianskoe-i-postnoe/', 'krupy-makarony-muka/',
              'osoboe-pitanie/', 'chay-i-kofe/', 'masla-sousy-spetsii-sakhar-i-sol/', 'konservatsiya/', 'alkogol/',
              'zdorove/', 'tovary-dlya-doma-i-kukhni/', 'kosmetika-sredstva-gigieny/', 'tovary-dlya-zhivotnykh/',
              'indilavka/', 'sad-i-ogorod/', 'dobraya-polka/']

for category in categories:
    parcing(category)
driver.quit()
print(all_products_from_VV)
