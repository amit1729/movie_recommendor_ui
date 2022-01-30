import scrapy
from twisted.internet import reactor
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from .spiders.spiders.spiders.gcextractor import preliminarySpider

def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run(installSignalHandlers=False)
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
