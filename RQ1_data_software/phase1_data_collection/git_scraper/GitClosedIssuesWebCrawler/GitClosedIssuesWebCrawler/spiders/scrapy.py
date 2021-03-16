import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from GitClosedIssuesWebCrawler.items import GitItem
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
    with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/github-closed-issue1_data.json') as f:
        d = json.load(f)
    with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/github-closed-issue2_data.json') as f:
        e = json.load(f)
    #print(columns['URL'])
    file_url = [item.get('url') for item in d]
    new_url = []
    for url in file_url:
        url = url.split('/issues')[0]
        new_url.append(url)
    file_url1 = [item.get('url') for item in e]
    new_url1 = []
    for url in file_url1:
        url = url.split('/issues')[0]
        new_url1.append(url)
    git_urls = [s for s in columns['URL'] if "github.com" in s]
    # print(len(git_urls))
    # print(len(set(new_url)))
    # print(len(set(new_url1)))
    # temp = new_url + new_url1
    # print(len(set(temp)))
    # temp1 = list(set(git_urls)-set(temp))
    # print(len(temp1))
    # output = list(set(git_urls) - set(new_url))
    # #print(len(output))
    # git_urls = output
    git_urls = [x + "/issues" for x in git_urls]
    git_issue_urls = [x + "?q=is%3Aissue+is%3Aclosed" for x in git_urls]
    # #print(git_issue_urls)
    # start_urls = ['https://github.com/youbot/youbot-ros-pkg/issues']
    start_urls = git_issue_urls

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pagination',)),
             callback="parse_link",
             follow=True),)

    # def parse(self, response):
    #     for link in self.git_issue_urls:
    #         #print(link)
    #         yield scrapy.Request(link, callback=self.parse_link)


    def parse_link(self, response):
        #print('Processing..' + response.url)
        open_issue_links = response.css('a.link-gray-dark.v-align-middle.no-underline.h4.js-navigation-open::attr(href)').extract()
        for a in open_issue_links:
            #print(a)
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        #print('Processing..' + response.url)
        item = GitItem()
        response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li > p::text').extract()
        response.css('td.d-block.comment-body.markdown-body.js-comment-body code::text').extract()

        url = response.url
        item['url'] = url
        issue_title = response.css('h1 span.js-issue-title::text').extract_first()
        issue_title = issue_title.strip()
        item['issue_title'] = issue_title
        item['issue_status'] = "Closed"
        posted_on = response.css('relative-time::text').extract_first()
        item['posted_on'] = posted_on
        issue_contents = response.css('td.d-block.comment-body.markdown-body.js-comment-body p::text').extract()
        item['issue_contents'] = issue_contents
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body code::text').extract():
            issue_code = response.css('td.d-block.comment-body.markdown-body.js-comment-body code::text').extract()
            item['issue_code'] = issue_code
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body > blockquote > p::text').extract():
            issue_quotes = response.css('td.d-block.comment-body.markdown-body.js-comment-body > blockquote > p::text').extract()
            item['issue_quotes'] = issue_quotes
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li > p::text').extract():
            contents_details = response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li > p::text').extract()
            item['contents_details'] = contents_details
        if response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li::text').extract():
            contents_details_more = response.css('td.d-block.comment-body.markdown-body.js-comment-body > ul > li::text').extract()
            contents_details_more = [ x for x in contents_details_more if "\n" not in x ] 
            item['contents_details_more'] = contents_details_more
        yield item