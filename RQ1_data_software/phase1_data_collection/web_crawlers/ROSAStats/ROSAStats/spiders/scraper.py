import scrapy
import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ROSAStats.items import RosaItem

class RosaSpider(CrawlSpider):
    name = "rosa"
    with open('../../../../data/rosa_data.json') as f:
        url_data = json.load(f)
    wiki_url = [item.get('url') for item in url_data]

    start_urls = wiki_url

    def parse(self, response):
        item = RosaItem()

        item['url'] = response.url

        user = response.css('.user-info a::text').extract_first()
        item['user'] = user
        print(user)
        
        yield item