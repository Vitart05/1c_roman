import re
import requests
from bs4 import BeautifulSoup
import csv
from settings import url_set


def first_str():
    with open('parser.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(('Код товара', 'Артикул', 'Наименование товара', 'Наличие шт', 'Цена руб'))


def get_price(s):
    pattern = r'\d{1,9}'
    salary = re.findall(pattern, s)
    salary1 = ''
    for sal in salary:
        salary1 = salary1 + sal
    return salary1


def write_csv(data):
    with open('parser.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow((data['product_code'],
                         data['article'],
                         data['name'],
                         data['count'],
                         data['price1'],))


def count_page():
    file = open('pages/page1.html').read()
    soup = BeautifulSoup(file, 'lxml')
    pages = soup.find_all('li', class_='pagination__pages-list-item')
    last_page = pages[-2].text.strip()
    return int(last_page)


def main():
    first_str()
    for k in range(1, count_page() + 1):
        file = open('pages/page{}.html'.format(str(k))).read()
        soup = BeautifulSoup(file, 'lxml')
        prices = soup.find_all('div', class_='catalog-section-items-item')
        for price in prices:
            product_code = price.find('div', class_='catalog-section-items-item__code').text.strip()
            article = price.find('div', class_='catalog-section-items-item__article').text.strip()
            name = price.find('span', class_='js-product-card').text.strip().strip('"')
            name = name.replace(',', '.')
            count1 = price.find('span', class_='catalog-section-items-item__available').text.strip()
            count = get_price(count1)
            if count == '':
                count = '0'
            pric = price.find('div', class_='catalog-section-items-item-price__value').text.strip()
            price1 = get_price(pric)
            data = {'product_code': product_code, 'article': article, 'name': name, 'count': count, 'price1': price1}
            write_csv(data)
        print(k)


if __name__ == '__main__':
    main()