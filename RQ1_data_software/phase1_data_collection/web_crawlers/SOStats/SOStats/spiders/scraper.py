import scrapy
import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SOStats.items import SOItem

class SOSpider(CrawlSpider):
    name = "stackoverflow"
    with open('../../../../data/stackoverflow_data.json') as f:
        url_data = json.load(f)
    so_url = [item.get('url') for item in url_data]

    start_urls = so_url

    def parse(self, response):
        item = SOItem()

        item['url'] = response.url

        user = response.css('.user-info a::text').extract_first()
        if 'edited' in user:
            print('user is edited')
            user = response.css('.user-info a::text')[-1].extract()
            item['user'] = user
        else:
            item['user'] = user
        print(user)
        
        yield item