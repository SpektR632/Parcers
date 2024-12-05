import os
import requests
from bs4 import BeautifulSoup

books = []


def get_links(url):
    """
    Парсинг с сайта книг с атрибутами для записи в БД
    :return: список книг с атрибутами
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти все теги с атрибутами книг
    img_tags = soup.find_all(class_="b-lazy product-image js-product-image")
    title_tag = soup.find_all(class_='product-name js-product-name')
    author_tag = soup.find_all(class_="product-author js-product-author")
    description_tag = soup.find_all(class_="product-about__text js-card-product-text")
    price_tag = soup.find_all(class_="price price--current")

    number = 1
    img_links = []
    for img, title, author, description, price in zip(img_tags, title_tag, author_tag, description_tag, price_tag):
        src = img.get('data-src')
        url = title.get('href')

        response = requests.get('https://bookbars.ru' + url)
        soup = BeautifulSoup(response.text, 'html.parser')
        attr_tag = soup.find_all(class_="list-info__label")
        param_tag = soup.find_all(class_="list-info__link")
        attr_books = {}
        for attr, param in zip(attr_tag, param_tag):
            if attr.text in ['ISBN:', 'Год издания:', 'Издательство:', 'BIC:']:
                attr_books[attr.text] = param.text
        attr_books['title'] = title.text.strip()
        attr_books['description'] = description.text.strip()

        attr_books['author'] = author.text.strip()
        attr_books['price'] = price.text.strip()

        books.append(attr_books)
        number += 1

        if src and src.startswith('http') and src[-3:].lower() in ['png', 'jpg']:
            img_links.append(src)
        elif src and src.startswith('/') and src[-3:].lower() in ['png', 'jpg']:
            # Преобразовать относительные ссылки в абсолютные
            img_links.append('https://bookbars.ru' + src)

    return img_links


def download_images(img_links, save_dir='images'):
    """
    Загрузка изображений и сохранение в папке 'images'
    :param img_links:
    :param save_dir: папка для сохранения изображений
    """
    if not os.path.exists(save_dir):  # Создание папки, если её нет
        os.makedirs(save_dir)

    for i, link in enumerate(img_links):
        response = requests.get(link)
        if response.status_code == 200:
            filename = os.path.join(save_dir, f'image_{i + 1}.jpg')
            with open(filename, 'wb') as f:
                f.write(response.content)



url = 'https://bookbars.ru/catalog/knigi/?sort=counter&method=desc&PAGEN_1=2'
img_links = get_links(url)
download_images(img_links)

