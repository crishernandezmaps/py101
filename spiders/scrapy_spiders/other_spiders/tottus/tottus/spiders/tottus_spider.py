# -*- coding: utf-8 -*-
import scrapy
from tottus.items import fields
import re
import time

regex = re.compile(r'[\n\r\t]')

N = 'tottus_spider'
L = 'https://www.tottus.cl/tottus/search/Ofertas/cat1580016' # cambiar esta URL por la que se desee en el menu de la seccion ofertas de Tottus.cl

def find_numbers(string_to_evaluate):
    x = [int(s) for s in re.findall(r'\b\d+\b', string_to_evaluate)]
    return x[0]

class TottusSpiderSpider(scrapy.Spider):
    name = N
    allowed_domains = ['www.tottus.cl']
    start_urls = [L]

    def parse(self,response):
        for href in response.xpath("//div[contains(@class,'caption-top-wrapper')]/a//@href"):
            u = 'https://www.tottus.cl' + href.extract()    
            yield scrapy.Request(u, callback=self.parse_dir_contents)                   

    def parse_dir_contents(self,response):
        response_str = str(response)
        # time.sleep(3)

        item = fields() 
        item['titulo'] = response.xpath("//div[contains(@class,'title')]/h5/text()").extract()[0]
        item['url'] = response_str.split('<200')[1].replace('>','').strip()
        item['precio'] = find_numbers(response.xpath("//span[contains(@class,'active-price')]/span/text()").extract()[0].replace('.',''))
        print(item)
        yield item 
