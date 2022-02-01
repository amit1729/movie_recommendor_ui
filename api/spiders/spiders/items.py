# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class gclData(scrapy.Item):
    data = scrapy.Field()

class Movie(scrapy.Item):
    name = scrapy.Field()
    release_date = scrapy.Field()
    grating = scrapy.Field()
    glikes = scrapy.Field()
    selected = scrapy.Field()