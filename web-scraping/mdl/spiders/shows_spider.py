import scrapy

class ShowsSpider(scrapy.Spider):
    name = 'shows'
    start_urls = [
        'http://mydramalist.com/discussions/recent_discussions',
    ]

    visited_lists = set()

    def parse(self, response):
        for href in response.css('.thread--discussion h4 a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                callback=self.parse_discussion)

        next_page = response.urljoin(response.css('.pagination a::attr(href)')[-1].extract())
        if not next_page == response.url:
            yield scrapy.Request(next_page,
                callback=self.parse)

    def parse_discussion(self, response):
        for href in response.css('a[title="MyDramaList"]::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href + '/completed'),
                callback=self.parse_dramalist)

        next_page = response.urljoin(response.css('.pagination a::attr(href)')[-1].extract())
        if not next_page == response.url:
            yield scrapy.Request(next_page,
                callback=self.parse_discussion)

    def parse_dramalist(self, response):
        if response.url not in self.visited_lists:
            self.visited_lists.add(response.url)
            names = [x
                for x in response.css('.sort1 span::text').extract()
                if x != '(airing)'
            ]
            ratings = response.css('.sort5::text').extract()

            for i in range(len(names)):
                yield { 'name': names[i], 'rating': ratings[i]}