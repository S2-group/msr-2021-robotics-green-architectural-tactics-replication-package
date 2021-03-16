import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ROSAWebCrawler.items import ROSAItem

class ROSASpider(CrawlSpider):
    name = "ros-answers"
    start_urls = ['https://answers.ros.org/questions/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.paginator',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        #print('Processing..' + response.url)
        item_links = response.css('.short-summary > h2 > a::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        item = ROSAItem()
        temp = []

        title = response.css('h1 > .js-editable-content::text').extract()[0].strip()
        item['title'] = title
        time = response.css('.box.statsWidget abbr::text').extract()[0].strip()
        item['time'] = time
        post_content = response.css('.post.js-question > .post-content > .post-body > .js-editable > .js-editable-content > p::text').extract()
        item['post_content'] = post_content
        answer = response.css('.post.answer > .post-content > .post-body > .js-editable > .js-editable-content > p::text').extract()
        item['answer'] = answer
        temp = response.css('.post.js-question li::text').extract()
        if all(p == ' ' for p in temp):
            pass
        else:
            question_details = response.css('.post.js-question li::text').extract()
            item['question_details'] = question_details
        temp = response.css('.post.answer li::text').extract()
        if all(p == ' ' for p in temp):
            pass
        else:
            answer_details = response.css('.post.answer li::text').extract()
            item['answer_details'] = answer_details

        item['url'] = response.url
        yield item