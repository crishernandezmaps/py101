import requests as req
from bs4 import BeautifulSoup

def making_soup(url):
    resp = req.get(url)
    c = resp.content
    soup = BeautifulSoup(c, features='lxml')
    return soup
