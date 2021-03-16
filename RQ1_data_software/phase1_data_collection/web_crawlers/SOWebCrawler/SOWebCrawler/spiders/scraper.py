import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SOWebCrawler.items import SOItem

class SOSpider(CrawlSpider):
    name = "stackoverflow"
    #allowed_domains = ["www.olx.com.pk"]
    start_urls = ['https://stackoverflow.com/questions/tagged/ros?tab=newest&pagesize=50']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pager',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        #print('Processing..' + response.url)
        item_links = response.css('.question-hyperlink::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        print('parse_detail_page')
        item = SOItem()

        title = response.css('.question-hyperlink::text').extract()[0].strip()
        item['title'] = title
        time = response.css('.user-action-time span::attr(title)').extract()[0].strip()
        item['time'] = time
        post_content = response.css('.question p::text').extract()
        item['post_content'] = post_content
        answer = response.css('.answer p::text').extract()
        item['answer'] = answer
        if response.css('blockquote > p::text').extract():
            quote = response.css('blockquote > p::text').extract()
            item['quote'] = quote
        if response.css('.question code::text').extract():
            question_code = response.css('.question code::text').extract()
            item['question_code'] = question_code
        if response.css('.answer code::text').extract():
            answer_code = response.css('.answer code::text').extract()
            item['answer_code'] = answer_code

        item['url'] = response.url
        yield item