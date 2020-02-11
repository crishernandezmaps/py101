# -*- coding: utf-8 -*-
import scrapy
from lider.items import fields
import re
import time

regex = re.compile(r'[\n\r\t]')

N = 'lider_spider'
L = 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Jugos/_/N-oz9aq9?No=40&isNavRequest=Yes&Nrpp=80' 

# aqui es copiar y pegar la categoria de donde se encuentra el producto. Se recomienda usar un VPN, ya que Lider bloquea inmediatamante.
list_of_urls = []
for x in range(0,320,80):
    w = L.split('?')[0] + '?No=' + str(x) + '&isNavRequest=Yes&Nrpp=80' 
    list_of_urls.append(w)

def find_numbers(string_to_evaluate):
    x = [int(s) for s in re.findall(r'\b\d+\b', string_to_evaluate)]
    return x[0]

class LiderSpiderSpider(scrapy.Spider):
    name = N
    allowed_domains = ['www.lider.cl']
    start_urls = list_of_urls

    def parse(self,response):
        for href in response.xpath("//div[contains(@class,'product-details')]/a//@href"):
            u = 'https://www.lider.cl' + href.extract()    
            yield scrapy.Request(u, callback=self.parse_dir_contents)                   

    def parse_dir_contents(self,response):
        response_str = str(response)
        # time.sleep(3)

        item = fields() 
        item['titulo'] = response.xpath("//div[contains(@class,'product-info col-lg-3 col-md-5 col-sm-5 col-xs-10')]/h1/span/text()").extract()[0]
        item['url'] = response_str.split('<200')[1].replace('>','').strip()
        item['descripcion'] = response.xpath("//span[contains(@id,'span-display-name')]/text()").extract()[0]
        item['precio'] = find_numbers(response.xpath("//p[contains(@class,'price')]/text()").extract()[0].replace('.',''))
        item['puntos_lider'] = response.xpath("//p[contains(@class,'miclub')]/text()").extract()[0].replace('\xa0Pesos','')
        print(item)
        yield item 
