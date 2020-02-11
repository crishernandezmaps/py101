import scrapy
from scraping.items import fields
import pandas as pd
import re
import json

n = 'arriendo_departamento'

class scraperApp(scrapy.Spider):
    name = n
    comunas = ['cerrillos']
    # comunas = [
    #     'santiago',
    #     'cerrillos',
    #     'cerro-navia',
    #     'conchali',
    #     'el-bosque',
    #     'estacion-central',
    #     'huechuraba',
    #     'independencia',
    #     'la-cisterna',
    #     'la-florida',
    #     'la-granja',
    #     'la-pintana',
    #     'la-reina',
    #     'las-condes',
    #     'lo-barnechea',
    #     'lo-espejo',
    #     'lo-prado',
    #     'macul',
    #     'maipu',
    #     'nunoa',
    #     'pedro-aguirre-cerda',
    #     'penalolen',
    #     'providencia',
    #     'pudahuel',
    #     'quilicura',
    #     'quinta-normal',
    #     'recoleta',
    #     'renca',
    #     'san-joaquin',
    #     'san-miguel',
    #     'san-ramon',
    #     'vitacura']

    list_of_urls = []
    for i in comunas:    
        for x in range(51, 3001, 50):
            url = f'https://www.portalinmobiliario.com/{n.split("_")[0]}/{n.split("_")[1]}/{i}-metropolitana'
            list_of_urls.append(url)
            list_of_urls.append(f'{url}/_Desde_{x}')

    start_urls = list_of_urls

    def parse(self, response):
        for href in response.xpath("//div[contains(@class,'image-content')]/a//@href"):
            u = href.extract()
            yield scrapy.Request(u, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        if response:
            response_str = str(response)
            source = response.xpath("//script[contains(., 'dynamicMapProperties')]/text()").extract()[0]
            item = fields()
            item['vivienda'] = n.split('_')[-1]
            item['tipo'] = response_str.split('/')[3]
            item['district'] = response_str.split('-metropolitana')[0].split('/')[-1]
            item['title'] = response.xpath("//h2[contains(@class,'map-address')]/text()").extract()[0].strip()
            item['broker'] = response.xpath("//div[contains(@class, 'modal__input modal__input--unregistered-question question__unregistered-question')]/textarea/text()").extract()[0].split('Hola')[1].split(',')[0].strip()
            item['direction'] = response.xpath("//h2[contains(@class,'map-address')]/text()").extract()[0].strip()
            item['supTotal'] = find_numbers(response.xpath("/html/body/main/div/div/div[1]/section[1]/div/div/div/section/ul/li[1]/span").extract()[0])
            item['supUtil'] = find_numbers(response.xpath("/html/body/main/div/div/div[1]/section[1]/div/div/div/section/ul/li[2]/span").extract()[0])
            item['valor'] = find_value(response.xpath("/html/body/main/div/div/div[2]/div[1]/section/div/div/fieldset/span/span[2]").extract()[0])
            item['fecha_publicacion'] = response.xpath("//div[contains(@class,'info-property-date')]/p[contains(@class,'info')]/text()").extract()[0]
            item['idCliente'] = response_str.split('/')[-1].split('-')[0]
            item['url'] = response_str.split('<200')[1].replace('>', '').strip()
            item['lat'] = find_coordinates_in_script(source)[0]
            item['lon'] = find_coordinates_in_script(source)[1]
            item['portal'] = 'Portal Inmobiliario'
            item['moneda'] = response.xpath('/html/body/main/div/div/div[2]/div[1]/section/div/div/fieldset/span/span[1]/text()').extract()[0]
            item['algo'] = 'algo'
            print(item)
            yield item
        else:
            pass


def find_numbers(string_to_evaluate):
    x = [int(s) for s in re.findall(r'\b\d+\b', string_to_evaluate)]
    return x[0]


def find_value(string_with_value):
    x = re.findall(r'\b\d+\b', string_with_value)
    return int('.'.join(x).replace('.', ''))


def get_values(parameter, script):
    return re.findall('%s = "(.*)"' % parameter, script)[0]


def find_coordinates_in_script(s):
    formated_source = s.replace('\n', '').replace('\t', '').replace(' ', '')
    string_to_find_coordinates = formated_source.split('center=')
    x_and_y = string_to_find_coordinates[1].split('&zoom')[0].split('%2C')
    return x_and_y  # [X,Y]
