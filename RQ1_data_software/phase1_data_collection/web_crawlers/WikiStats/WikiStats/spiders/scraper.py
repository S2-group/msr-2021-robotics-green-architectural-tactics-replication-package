import scrapy
import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from WikiStats.items import WikiItem

class WikiSpider(CrawlSpider):
    name = "wiki"
    with open('../../../../data/wiki_data.json') as f:
        url_data = json.load(f)
    wiki_url = [item.get('url') for item in url_data]

    start_urls = wiki_url

    def parse(self, response):
        item = WikiItem()

        item['url'] = response.url

        e_time = response.css('p.info::text').extract_first()
        time = re.search('edited(.*)by', e_time)
        time = time.group(1)
        time = time.strip()
        item['time'] = time
        print(time)

        e_user = response.css('p.info a::attr(href)')[-1].extract()
        user = e_user[1:]
        item['user'] = user
        print(user)
        
        yield item