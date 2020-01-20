# -*- coding: utf-8 -*-
import scrapy

class fields(scrapy.Item):
    title = scrapy.Field()
    precio_unitario = scrapy.Field()
    precio_caja = scrapy.Field()
    pass
