import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from WikiCrawler.items import WikiItem

class WikiSpider(CrawlSpider):
    name = "wiki"
    with open('urls.json') as f:
        url_data = json.load(f)
    url = [item.get('urls') for item in url_data]
    wiki_url = ['https://wiki.ros.org/{0}'.format(i) for i in url]
    # start_urls = ['https://wiki.ros.org/resource_retriever']
    start_urls = wiki_url
    print('hello')


    def parse(self, response):
        print('hello0')
        item = WikiItem()
        package_details1 = []
        package_details2 = []

        item['url'] = response.url

        package = response.css('a.backlink::text').extract_first()
        item['package'] = package

        button = response.css('[id="rosversion_selector"] button::text').extract_first()
        button = button.strip()
        ros_version = '.version.'+button
        package_summary = response.css(ros_version+' p::text').extract()
        item['package_summary'] = package_summary

        if response.css('[id="content"] > p.line867::text').extract():
            package_details1 = response.css('[id="content"] > p.line867::text').extract()

        if response.css('[id="content"] > p.line862::text').extract():
            package_details2 = response.css('[id="content"] > p.line862::text').extract()

        if (len(package_details1) != 0 and len(package_details2) != 0):
            package_details = package_details1 + package_details2
            item['package_details'] = package_details

        elif (len(package_details1) != 0 and len(package_details2) == 0):
            package_details = package_details1
            item['package_details'] = package_details

        elif (len(package_details1) == 0 and len(package_details2) != 0):
            package_details = package_details2
            item['package_details'] = package_details

        if response.css('[id="page"] tt::text').extract():
            package_tt = response.css('[id="page"] tt::text').extract()
            item['package_tt'] = package_tt

        if response.css('[id="page"] pre::text').extract():
            package_code = response.css('[id="page"] pre::text').extract()
            item['package_code'] = package_code

        print(package_summary)
        yield item