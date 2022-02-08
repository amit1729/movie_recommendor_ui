import scrapy
from scrapy.utils.response import open_in_browser
from ..items import gclData
from ..pipelines import PermilinaryDataPipeline

class preliminarySpider(scrapy.Spider):
    name = "preliminary"
    start_urls = [
        'https://www.imdb.com/search/title/',
    ]


    def __init__(self,**kwargs):
        print("Running  spider...")
        self.pipeline = PermilinaryDataPipeline()

 
    def parse(self, response):
        genres1 = response.xpath('//input[@name = "genres"]/..//label/text()').extract()
        genres = []
        for genre in genres1:
            genres.append(genre.strip())
        genres.sort()
        data = {}
        data['genres'] = genres
        #category
        cat1 = response.xpath('//div[@class="inputs"]/table/tbody/tr/td/label/text()').extract()[:14]
        #cat1 = response.xpath('//input[@name = "title_type"]/..//label/text()').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        data['TitleTypes'] = cats
        #language
        cat1 = response.xpath('//select[@name = "languages"]/option/text()').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        data['language'] = cats
        #language_Values
        cat1 = response.xpath('//select[@name = "languages"]/option/@value').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        data['language_values'] = cats
        #category_Values
        cat1 = response.xpath('//input[@name = "title_type"]/@value').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        data['TitleTypes_values'] = cats
        #Genre_Values
        cat1 = response.xpath('//input[@name = "genres"]/@value').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        data['genres_values'] = cats
        #certificates
        cat1 = response.xpath('//input[@name = "certificates"]/@value').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        data['certificates'] = cats
        self.pipeline.process_item(gclData(data=data),self)
        

