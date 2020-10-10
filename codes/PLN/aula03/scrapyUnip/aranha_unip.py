# -*- coding: utf-8 -*-
import scrapy


class AranhaUnipSpider(scrapy.Spider):
    name = 'aranha_unip'
    allowed_domains = ['http://www.vagalume.com.br']
    start_urls = ['http://http://www.vagalume.com.br/']

    def parse(self, response):
        pass
