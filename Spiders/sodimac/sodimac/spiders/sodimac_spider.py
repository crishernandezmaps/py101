# -*- coding: utf-8 -*-
import scrapy
from sodimac.items import fields
import re
import time

regex = re.compile(r'[\n\r\t]')

N = 'sodimac_spider'

CATEGORY_AND_NAME = 'cat340052/Hidrolavadoras-y-Accesorios'

list_of_urls = []
for x in range(0,176,16):
    nl = f'https://www.sodimac.cl/sodimac-cl/category/{CATEGORY_AND_NAME}?No={x}&Nrpp=16'
    list_of_urls.append(nl)

def find_numbers(string_to_evaluate):
    x = [int(s) for s in re.findall(r'\b\d+\b', string_to_evaluate)]
    return x[0]

class SodimacSpider(scrapy.Spider):
    name = N
    allowed_domains = ['www.sodimac.cl']
    start_urls = list_of_urls

    def parse(self,response):
        for href in response.xpath("//p[contains(@class,'name jq-name')]/a//@href"):
            u = ('https://www.sodimac.cl' + href.extract()).replace(',','')      
            yield scrapy.Request(u, callback=self.parse_dir_contents)                   

    def parse_dir_contents(self,response):
        response_str = str(response)
        # time.sleep(3)

        item = fields() 
        item['titulo'] = response.xpath("//h1[contains(@class,'name')]/span/text()").extract()[0].replace('\xa0',' ')
        item['precio_unitario'] = find_numbers(response.xpath("/html/body/main/section/section[1]/div/div[2]/div[1]/div/div[1]/p[2]").extract()[0].replace('.',''))
        item['zona'] = regex.sub('', response.xpath("//a[contains(@class,'jq-cambiar hidden-xs hidden-sm zone-price-name regionName')]/span/text()").extract()[0])
        item['url_aviso'] = response_str.split('<200')[1].replace('>','').strip()
        item['puntos_cmr'] = find_numbers(response.xpath("//p[contains(@class,'acumulas')]/text()").extract()[0].replace('.',''))
        print(item)
        yield item         


# import code; code.interact(local=dict(globals(), **locals()))     

'''
INSTRUCCIONES:
- Scroll down hasta la ultima pagina.
- Copiar el link resultante de la pagina final.
- cambiar el contenido de la variable L por el link copiado anteriormente.
'''