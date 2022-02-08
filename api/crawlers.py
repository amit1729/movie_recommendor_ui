from twisted.internet import reactor
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from scrapy.utils.log import configure_logging
from .spiders.spiders.spiders.gcextractor import preliminarySpider
from .spiders.spiders.spiders.IMDbSpider import IMDbSpider
from asgiref.sync import sync_to_async

def run_spider(spider,**kwargs):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider,**kwargs)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

def crawlSetup():
  run_spider(preliminarySpider)

def crawlMovies(urls,movieLimit,gLikes):
    run_spider(IMDbSpider,urls=urls,movieLimit=movieLimit,gLikes=gLikes)
