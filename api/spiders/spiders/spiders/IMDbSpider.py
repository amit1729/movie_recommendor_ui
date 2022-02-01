import scrapy
from scrapy.utils.response import open_in_browser
from ..items import Movie
class IMDbSpider(scrapy.Spider):
  name = "imdbspider"
  
  def __init__(self,**kwargs):
    self.start_urls = kwargs["urls"]
    self.movieLimit = kwargs["movieLimit"]



  def process_dates(self,dates):
        processed_dates = []
        for date in dates:
            date = date.split()
            tdate = ""
            if len(date) == 2:
                tdate = date[1]
            else:
                tdate = date[0]
            processed_dates.append(tdate)
        return processed_dates


  def parse(self, response, index = 0):
    imdb_lim = self.movieLimit
    movie_names = response.xpath('//div[@class = "lister list detail sub-list"]//h3[@class="lister-item-header"]/a/text()').extract()
    release_years = response.xpath('//div[@class = "lister list detail sub-list"]//h3[@class="lister-item-header"]/span[@class="lister-item-year text-muted unbold"]/text()').extract()
    index+=len(movie_names)
    if(len(movie_names)<50):
      next_page = None
    else:
      next_page = response.xpath('//div[@class = "desc"]/a[@class="lister-page-next next-page"]/@href').extract()[0]
    if(index>imdb_lim):
      del movie_names[-index+imdb_lim:]
      del release_years[-index+imdb_lim:]
      index = 0
      next_page =None
    else:
      next_page = response.xpath('//div[@class = "desc"]/a[@class="lister-page-next next-page"]/@href').extract()[0]
        #print("\n")
        #print(movie_names)
        #print("\n")
    release_years = self.process_dates(release_years)
        #print(len(movie_names))
    for (m,r) in zip(movie_names, release_years):
      yield self.dp.process_item(Movie(name=m, release_date=r),self)
    print(next_page)
    if next_page is not None:
      print("going to next page ....")
      next_page = response.urljoin(next_page)
      yield scrapy.Request(next_page, callback=self.parse, cb_kwargs={'index':index})
    else:
      index = 0
        
    if(index>=imdb_lim):
      index=0
      pass