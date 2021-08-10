import requests
from bs4 import BeautifulSoup
from settings import url_set

i = 1
while True:
    pagelink = url_set + '?page={}'.format(str(i))
    page = requests.get(pagelink)
    soup = BeautifulSoup(page.text, 'lxml')
    with open('pages/page{}.html'.format(str(i)), 'a') as file:
        file.write(page.text)
    pages = soup.find('a', class_='pagination__nav-link pagination__nav-link_next')
    if pages:
        i += 1
    else:
        break
    print(pagelink)