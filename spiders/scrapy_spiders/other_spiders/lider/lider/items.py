# -*- coding: utf-8 -*-
import scrapy

class fields(scrapy.Item):
    # test = scrapy.Field()
    titulo = scrapy.Field()
    url = scrapy.Field()
    descripcion = scrapy.Field()
    precio = scrapy.Field()
    puntos_lider = scrapy.Field()
    pass
