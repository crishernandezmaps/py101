import scrapy

class fields(scrapy.Item):
	vivienda = scrapy.Field() 
	tipo = scrapy.Field()
	district = scrapy.Field()
	title = scrapy.Field()
	broker = scrapy.Field()
	direction = scrapy.Field()
	supTotal = scrapy.Field()
	supUtil = scrapy.Field()
	valor = scrapy.Field()
	fecha_publicacion = scrapy.Field()
	idCliente = scrapy.Field()
	url = scrapy.Field()
	lat = scrapy.Field()
	lon = scrapy.Field()
	portal = scrapy.Field()
	moneda = scrapy.Field()
	algo = scrapy.Field()