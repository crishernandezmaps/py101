import requests as req
from bs4 import BeautifulSoup
import random
import sys
import re
import pandas as pd

def making_soup(u):
    try:
        uas = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
               "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
               "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
               )
        ua = uas[random.randrange(len(uas))]
        headers = {'user-agent': ua}
        resp = req.get(u, headers=headers)
        c = resp.content
        soup = BeautifulSoup(c, features='lxml')
        return soup
    except req.exceptions.HTTPError as e:
        print(e)
        sys.exit(1)

def find_numbers(string_to_evaluate):
    x = [int(s) for s in re.findall(r'\b\d+\b', string_to_evaluate)]
    return x[0]


def main():

    comunas = ['pudahuel','cerrillos','cerro-navia','conchali','el-bosque',
    'estacion-central','huechuraba','independencia','la-cisterna','la-florida',
    'la-granja','la-pintana','la-reina','las-condes','lo-barnechea','lo-espejo',
    'lo-prado','macul','maipu','nunoa','pedro-aguirre-cerda','penalolen',
    'providencia','renca','quilicura','quinta-normal','recoleta','santiago',
    'san-joaquin','san-miguel','san-ramon','vitacura']

    list_of_urls = []
    for i in comunas[0:1]:    
        for x in range(51, 3001, 50):
            url = f'https://www.portalinmobiliario.com/arriendo/departamento/{i}-metropolitana'
            list_of_urls.append(url)
            list_of_urls.append(f'{url}/_Desde_{x}')

    properties_url = []
    for j in list_of_urls:
        s = making_soup(j)
        for i in s.find_all('a', class_='item__info-link'):
            p_url = i['href']
            p_soup = making_soup(p_url)
            for k in p_soup.find_all('h1', class_='item-title__primary'):
                try:
                    comuna = p_url.split('-metropolitana')[0].split('/')[-1]
                    codigo = p_url.split('-metropolitana')[1].split('-')[0].replace('/','').strip()
                    title = (k.text).strip()
                    precio = (p_soup.find('span', class_='price-tag-fraction').text).strip()
                    tipo = 'departamento'
                    informacion = [comuna, codigo, precio, tipo]
                    properties_url.append(informacion)
                    print(f'Info: {informacion}')
                
                except Exception as e:
                    print(e)
                    pass
    
    df = pd.DataFrame.from_records(properties_url)
    df.rename(columns={0:'comuna', 1:'codigo', 2:'precio', 3:'tipo'}, inplace=True)
    df.to_csv('deptos.csv')
    print(df.head())

# x = 'https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana/5390583-edificio-carmen-oriente-110-carmen-santiago-uda#position=50&type=item&tracking_id=e05684db-e790-431a-bacf-38f18ea3f65e'


if __name__ == "__main__":
    main()
    pass        