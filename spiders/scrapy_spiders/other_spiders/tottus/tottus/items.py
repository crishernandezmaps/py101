# -*- coding: utf-8 -*-
import scrapy

class fields(scrapy.Item):
    titulo = scrapy.Field()
    url = scrapy.Field()
    precio = scrapy.Field()
    pass
