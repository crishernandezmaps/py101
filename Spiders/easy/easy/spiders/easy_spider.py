# -*- coding: utf-8 -*-
import scrapy
from easy.items import fields

N = 'easy_spider'
L = "https://www.easy.cl/tienda/categoria/maderas-y-tableros-?cur_page=1&cur_view=grid&cur_pos="
# L = "https://www.sodimac.cl/sodimac-cl/category/cat4850444/?cid=esp105434"

class EasySpiderSpider(scrapy.Spider):
    name = N
    # allowed_domains = ['www.sodimac.cl']
    allowed_domains = ['www.easy.cl']
    start_urls = [L]

    def parse(self,response):
        for href in response.xpath("//div[contains(@class,'product')]/a[contains(@class,'product_image')]//@href"):
            u = 'https://www.easy.cl' + href.extract() 
            yield scrapy.Request(u, callback=self.parse_dir_contents)                   

    def parse_dir_contents(self,response):
        item = fields() 
        item['title'] = response.xpath("//h1[contains(@class,'product-details__title')]/text()").extract()[0]
        # item['precio_unitario'] = response.xpath("//span[contains(@class,'mt2-price-text')]/text()").extract()[0].replace('.','')
        # item['precio_caja'] = response.xpath("//div[contains(@class,'mt2-cajaPrice')]/text()").extract()[0].replace('\t','').replace('\r','').replace('\n','').replace('\xa0Caja',' ').replace('$','').replace('.','')
        print(item)
        yield item  

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

    # def parse(self,response):
    #     for href in response.xpath("//p[contains(@class,'name jq-name')]/a//@href"):
    #         u = ('https://www.sodimac.cl' + href.extract()).replace(',','')      
    #         yield scrapy.Request(u, callback=self.parse_dir_contents)                   

    # def parse_dir_contents(self,response):
    #     item = fields() 
    #     item['title'] = response.xpath("//h1[contains(@class,'name')]/span/text()").extract()[0].replace('\xa0',' ')
    #     item['precio_unitario'] = response.xpath("//span[contains(@class,'mt2-price-text')]/text()").extract()[0].replace('.','')
    #     item['precio_caja'] = response.xpath("//div[contains(@class,'mt2-cajaPrice')]/text()").extract()[0].replace('\t','').replace('\r','').replace('\n','').replace('\xa0Caja',' ').replace('$','').replace('.','')
    #     print(item)
    #     yield item         

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

# import code; code.interact(local=dict(globals(), **locals()))     

'''
INSTRUCCIONES:
- Scroll down hasta la ultima pagina.
- Copiar el link resultante de la pagina final.
- cambiar el contenido de la variable L por el link copiado anteriormente.
'''