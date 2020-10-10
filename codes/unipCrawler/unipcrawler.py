import scrapy

class unipCrawler(scrapy.Spider):
   name = "unipXereta"
   starts_urls = ['https://g1.globo.com/']

   def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            pass
