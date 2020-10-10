# -*- coding: utf-8 -*-
import scrapy


class AranhaUnipSpider(scrapy.Spider):
    name = 'aranha_unip'
    allowed_domains = ['https://www.vagalume.com.br/top100/']
    start_urls = ['https://www.vagalume.com.br/top100/']

    def parse(self, response):
        print(response.url)
        linksDaPagina = response.xpath("//a")


        for l in linksDaPagina:
            text = l.xpath("text()").extract_first()
            link = l.xpath("@href").extract_first()
            request = response.follow(link, callback=self.parse)
            yield request
