import scrapy


class GumSpider(scrapy.Spider):
    name = 'Gum'
    allowed_domains = ['https://g1.globo.com/']
    start_urls = ['http://https://g1.globo.com//']

    def parse(self, response):
        pass
