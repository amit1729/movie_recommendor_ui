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
    movie_id = scrapy.Field()
    name = scrapy.Field()
    imdbLikes = scrapy.Field()
    img_url = scrapy.Field()
    release_date = scrapy.Field()
    glikes = scrapy.Field()