import scrapy


class RdwsItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    
