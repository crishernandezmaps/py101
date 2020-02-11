import requests as req
from bs4 import BeautifulSoup
import wget
import pandas as pd

def making_soup(url):
    resp = req.get(url)
    c = resp.content
    soup = BeautifulSoup(c, features='lxml')
    return soup

seia = 'https://seia.sea.gob.cl/expediente/ficha/fichaPrincipal.php?modo=ficha&id_expediente=2145325740'
seia_dos = 'https://seia.sea.gob.cl/expediente/ficha/fichaPrincipal.php?modo=ficha&id_expediente=2142543029'
servel = 'https://www.servel.cl/padron-electoral-auditado-plebiscito-nacional-2020/'

# Generating list of codes
df = pd.read_html('https://zeus.sii.cl/avalu_cgi/br/brch10.sh')
table_codes = df[-1]
list_of_codes = table_codes[0][1:].values

for i in list_of_codes:
    try:
        pdf_url = f"https://www.servel.cl/wp-content/uploads/2020/01/A{i}.pdf"
        print(f'Downloading {i}')
        wget.download(pdf_url)
        print(pdf_url)
    except:
        pass

"""
def inside_project(u):
    my_soup = making_soup(u)
    list_of_a_tags = my_soup.find_all('a')
    href_list = []
    for i in list_of_a_tags:
        try:
            to_inspect = i['href']
            if to_inspect.split('/')[0] == 'https:':
                print(to_inspect)
        except:
            pass

# inside_project('https://seia.sea.gob.cl/expediente/ficha/fichaPrincipal.php?modo=ficha&id_expediente=2131221518')

# Sbif
def get_file_from_sbif(code):
    base_code = f'InfoFinanciera?indice=C.D.A&idContenido={code}'
    base_url = 'https://www.sbif.cl/sbifweb/servlet/'
    base = 'https://www.sbif.cl/'
    s = making_soup(f'{base_url}{base_code}')
    for i in s.find_all('a'):
        if i['href'].split('.')[-1] == 'xlsx' or i['href'].split('.')[-1] == 'xls': 
            p = i['href'][6:]
            to_download = f'{base}{p}'
            print(to_download)
            wget.download(to_download)
            print(to_download)

l = ['10648']
for i in l:
    get_file_from_sbif(i)            
"""    