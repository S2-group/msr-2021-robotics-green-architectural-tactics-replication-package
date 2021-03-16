import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from GitOpenPRWebCrawler.items import GitItem
import csv
import json
from collections import defaultdict

####################################
#### REMOVE BLANK LINES FROM CSV ###
####################################
def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

class GitSpider(CrawlSpider):
    name = "github"
    columns = defaultdict(list)
    with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/Repos_all.csv') as f:
      reader = csv.DictReader(no_blank(f))
      for row in reader:
          for (k,v) in row.items(): 
              columns[k].append(v)

    while '' in columns['URL']:
        columns['URL'].remove('')
    with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/github-open-pr-pagination_data.json') as f:
        d = json.load(f)
    with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/github-open-pr-no-pagination_data.json') as f:
        e = json.load(f)
    file_url = [item.get('url') for item in d]
    new_url = []
    for url in file_url:
        url = url.split('/pull')[0]
        new_url.append(url)
    file_url1 = [item.get('url') for item in e]
    new_url1 = []
    for url in file_url1:
        url = url.split('/pull')[0]
        new_url1.append(url)
    #print(columns['URL'])
    git_urls = [s for s in columns['URL'] if "github.com" in s]
    # print(len(git_urls))
    # print(len(set(new_url)))
    # print(len(set(new_url1)))
    # temp = new_url + new_url1
    # print(len(set(temp)))
    # temp1 = list(set(git_urls)-set(temp))
    # print(len(temp1))
    #output = list(set(git_urls) - set(new_url))
    #print(output)
    #print(len(output))
    #print(len(set(new_url)))
    # git_urls = output
    git_urls = [x + "/pulls" for x in git_urls]
    git_pr_urls = [x + "?q=is%3Aopen+is%3Apr" for x in git_urls]
    #print(git_issue_urls)
    start_urls = ['https://github.com/youbot/youbot-ros-pkg/issues']
    start_urls = git_pr_urls
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pagination',)),
             callback="parse_link",
             follow=True),)

    # def parse(self, response):
    #     temp = ['https://github.com/chrisl8/ArloBot/pulls?q=is%3Aopen+is%3Apr', 
    #     'https://github.com/anqixu/ueye_cam/pulls?q=is%3Aopen+is%3Apr',
    #     'https://github.com/ANYbotics/elevation_mapping/pulls?q=is%3Aopen+is%3Aprs']
    #     for link in self.git_pr_urls:
    #         #print(link)
    #         yield scrapy.Request(link, callback=self.parse_link)


    def parse_link(self, response):
        #print('Processing..' + response.url)
        open_pr_links = response.css('a.link-gray-dark.v-align-middle.no-underline.h4.js-navigation-open::attr(href)').extract()
        #open_pr_links = ['https://github.com/chrisl8/ArloBot/pull/106', 'https://github.com/anqixu/ueye_cam/pull/77']
        for a in open_pr_links:
            print(a)
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        print('Processing..' + response.url)
        #item = GitItem()
        item = {}
        count = 0
        url = response.url
        item['url'] = url
        pr_title = response.css('h1 span.js-issue-title::text').extract_first()
        pr_title = pr_title.strip()
        item['pr_title'] = pr_title
        username = response.css('a.author.text-bold.link-gray::text').extract_first()
        item['username'] = username
        username_url = response.css('a.author.text-bold.link-gray::attr(href)').extract_first()
        item['username_url'] = username_url
        item['issue_status'] = "Open"
        posted_on = response.css('relative-time::text').extract_first()
        item['posted_on'] = posted_on
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body p::text').extract():
            pr_contents = response.css('td.d-block.comment-body.markdown-body.js-comment-body p::text').extract()
            item['pr_contents'] = pr_contents
        if response.css('.js-comments-holder > p::text').extract():
            pr_comments = response.css('.js-comments-holder > p::text').extract()
            item['pr_comments'] = pr_comments
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body code::text').extract():
            pr_code = response.css('td.d-block.comment-body.markdown-body.js-comment-body code::text').extract()
            item['pr_code'] = pr_code
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body > blockquote > p::text').extract():
            pr_quotes = response.css('td.d-block.comment-body.markdown-body.js-comment-body > blockquote > p::text').extract()
            item['pr_quotes'] = pr_quotes
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li > p::text').extract():
            pr_details = response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li > p::text').extract()
            item['pr_details'] = pr_details
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li::text').extract():
            pr_details_more = response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li::text').extract()
            pr_details_more = [ x for x in pr_details_more if "\n" not in x ]
            item['pr_details_more'] = response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li::text').extract()
        # for k, v in item.copy().items():
        #     if v == 'renovate' or v == 'https://github.com/apps/renovate':
        #         count = count + 1
        #         del item
        #print('count: ', count)
        #if (username != 'renovate' and username_url != '/apps/renovate'):
        yield item