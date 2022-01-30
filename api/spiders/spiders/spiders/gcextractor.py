import scrapy
import json
from scrapy.utils.response import open_in_browser

class preliminarySpider(scrapy.Spider):
    name = "preliminary"
    start_urls = [
        'https://www.imdb.com/search/title/',
    ]

    def parse(self, response):
        genres1 = response.xpath('//input[@name = "genres"]/..//label/text()').extract()
        #print(response)
        genres = []
        for genre in genres1:
            genres.append(genre.strip())
        genres.sort()
        #print(genres)
        data = {}
        data['genres'] = genres
        #category
        cat1 = response.xpath('//div[@class="inputs"]/table/tbody/tr/td/label/text()').extract()[:14]
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        #print(cats)
        data['TitleTypes'] = cats
        #language
        cat1 = response.xpath('//select[@name = "languages"]/option/text()').extract()
        cats = []
        for c in cat1:
            cats.append(c.strip())
        cats.sort()
        #print(cats)
        data['language'] = cats
        with open('preliminary', 'w') as outfile:
            json.dump(data, outfile)

