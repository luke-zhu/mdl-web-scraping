import scrapy
import string
# import time

class ShowInfoSpider(scrapy.Spider):
    name = "show_info"
    start_urls = [
        'http://mydramalist.com/shows/alpha?letter=' + x
        for x in string.ascii_uppercase
    ]

    def parse(self, response):
        """
        for href in response.css('.title a::attr(href)'):
            yield scrapy.Request(href,
                callback=self.parse_show)
        """
        ratings = response.css('.statsInfo li b::text').extract()
        titles = [
            title
            for title in response.css('.title a::text').extract()
            if not title == 'add'
        ]

        for i in range(len(ratings)):
            yield { 'title': titles[i], 'avg_rating': ratings[i] }

        next_page = response.css('.pagination a::attr(href)')[-1].extract()
        if not next_page == response.url:
            yield scrapy.Request(next_page,
                callback=self.parse)
