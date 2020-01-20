# -*- coding: utf-8 -*-
import scrapy

class fields(scrapy.Item):
    titulo = scrapy.Field()
    precio_unitario = scrapy.Field()
    zona = scrapy.Field()
    url_aviso = scrapy.Field()
    puntos_cmr = scrapy.Field()
    pass