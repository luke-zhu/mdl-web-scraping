import scrapy

class RatingsSpider(scrapy.Spider):
    name = 'ratings'
    start_urls = [
        'http://mydramalist.com/discussions/recent_discussions',
    ]

    visited_lists = set()

    def parse(self, response):
        for href in response.css('.thread--discussion h4 a::attr(href)').extract():
            yield scrapy.Request(
                response.urljoin(href),
                callback=self.parse_discussion,
            )
        if response.css('.pagination a::attr(href)'):
            next_page = response.urljoin(response.css('.pagination a::attr(href)')[-1].extract())
            if next_page != response.url:
                yield scrapy.Request(
                    next_page,
                    callback=self.parse,
                )

    def parse_discussion(self, response):
        for href in response.css('a[title="MyDramaList"]::attr(href)').extract():
            if href not in self.visited_lists:
                self.visited_lists.add(href)
                yield scrapy.Request(
                    response.urljoin(href + '/completed'),
                    callback=self.parse_dramalist,
                )

        if response.css('.pagination a::attr(href)'):
            next_page = response.urljoin(response.css('.pagination a::attr(href)')[-1].extract())
            if next_page != response.url:
                yield scrapy.Request(
                    next_page,
                    callback=self.parse_discussion,
                )

    def parse_dramalist(self, response):
        for show in response.css('tr'):
            yield {
                'title': show.css('.sort1 span::text')[0].extract(),
                'country': show.css('.sort2::text')[0].extract(),
                'year': show.css('.sort3::text')[0].extract(),
                'type': show.css('.sort4::text')[0].extract(),
                'score': show.css('.sort5::text')[0].extract(),
                'user': response.url.split('/')[-2],
            }