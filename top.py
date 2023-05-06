from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv, xlrd

browser = webdriver.Firefox()
browser.get("https://www.kinopoisk.ru/lists/movies/top250/")
html = browser.page_source
browser.close()


soup = BeautifulSoup(html, "lxml")
movie_names_list = []
info_list = []
movie_info_list = []

movie_info = soup.find_all("div", "desktop-list-main-info_secondaryTitleSlot__mc0mI")
movie_names = soup.find_all("span", "styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj")

def get_movie():
    for names in movie_names:
        movie_names_list.append(names.text)

    for info in movie_info:
        info_list.append(info.text)

    for f in info_list:
        f = f.replace(u'\xa0', u' ')
        movie_info_list.append(f)
        result = [' - '.join(x) for x in zip(movie_names_list, movie_info_list)]
    return result
res = get_movie()

def get_xl():
    pd.DataFrame(res).to_excel('data.xlsx', header=False, index=False)

def get_csv():
    with open('data.csv', 'w', encoding='utf8', newline='') as f:
        w = csv.writer(f)
        w.writerow(res)

question = input("""В каком формате Вы бы хотели получить список?
1. Вывести список здесь
2. В формате excel
3. В формате csv
Выберите цифру: """)

if question == str(1):
    print('\n'.join(res))

elif question == str(2):
    get_xl()

elif question == str(3):
    get_csv()
    
