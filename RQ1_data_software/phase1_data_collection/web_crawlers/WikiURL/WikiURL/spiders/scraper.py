import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from WikiURL.items import WikiItem

class WikiSpider(CrawlSpider):
    name = "wikiurl"
    start_urls = ['https://index.ros.org/packages/page/1/time/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('ul.pagination.pagination-sm',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        new_urls = []
        print('Processing..' + response.url)
        item = WikiItem()
        item_links = response.css('.table-responsive > table.table.table-condensed.table-striped.table-hover > tbody > tr > td a::attr(href)').extract()
        for link in item_links:
            new_link = link.rsplit('/', 1)[-1]
            print(new_link)
            new_urls.append(new_link)
        new_urls = list(set(new_urls))
        for link in new_urls:
            item['urls'] = link
            yield item