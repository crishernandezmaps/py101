import requests as req
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time

em = 'https://www.elmostrador.cl/noticias/pais/2019/10/'

def making_soup(url):
    resp = req.get(url)
    c = resp.content
    soup = BeautifulSoup(c, features='lxml')
    return soup


def el_mostrador(link_to_em):
    s = making_soup(link_to_em)
    section = s.find_all('article', {'class': 'row'})

    list_of_link = []
    for article in section:
        div = article.find_all('div', {'class': 'col-xs-7 col-sm-10 col-md-10'})
        for a in div:
            a = a.find_all('a')[0]['href']
            list_of_link.append(a)

    return list_of_link

test = el_mostrador('https://www.elmostrador.cl/noticias/pais/2020/1/')
print(test)