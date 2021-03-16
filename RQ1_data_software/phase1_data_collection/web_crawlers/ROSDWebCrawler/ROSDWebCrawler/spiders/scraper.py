import scrapy
import sys
import urllib.request, json
from urllib.request import urlopen
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ROSDWebCrawler.items import ROSDItem

class ROSDSpider(CrawlSpider):
    name = "ros-discourse"
    start_urls = ['https://discourse.ros.org']
    all_urls = [  'https://discourse.ros.org/c/humanoids/35',
                  'https://discourse.ros.org/c/robot-description-formats/7',
                  'https://discourse.ros.org/c/ariac-users/24',
                  'https://discourse.ros.org/c/maritime/36',
                  'https://discourse.ros.org/c/aerial-vehicles/14',
                  'https://discourse.ros.org/c/turtlebot/12',
                  'https://discourse.ros.org/c/perception/30',
                  'https://discourse.ros.org/c/ros-industrial/39',
                  'https://discourse.ros.org/c/drivers/54',
                  'https://discourse.ros.org/c/buildfarm/20',
                  'https://discourse.ros.org/c/quality/37',
                  'https://discourse.ros.org/c/uncategorized/1',
                  'https://discourse.ros.org/c/release/16',
                  'https://discourse.ros.org/c/embedded/9',
                  'https://discourse.ros.org/c/client-libraries/22',
                  'https://discourse.ros.org/c/multi-robot-systems/60',
                  'https://discourse.ros.org/c/openembedded/26',
                  'https://discourse.ros.org/c/moveit/13'
                  'https://discourse.ros.org/c/general/8',
                  'https://discourse.ros.org/c/ros-projects/10',
                  'https://discourse.ros.org/c/autoware/46',
                  'https://discourse.ros.org/c/ng-ros/25'
                  ]
    page_number = 0
    all_data = []
    #?page="+str(page_number)
    data = []
    for page_number in range(1,20):   
      with urllib.request.urlopen("https://discourse.ros.org/c/ng-ros/25/l/latest.json") as url:
        data = json.loads(url.read().decode())

      # get the slug ursl to crawl
      urls = [url['slug'] for url in data['topic_list']['topics']]
      urls = list(map('https://discourse.ros.org/t/'.__add__,urls))
      all_data.append(urls)
      # print(urls)

    def parse(self, response):
      for items in self.all_data:
        for link in items:
          #print(link)
          yield scrapy.Request(link, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        #create items to store scraped contents
        item = ROSDItem()
        temp = []
        #scrape title of post
        title = response.css('h1 > a::text').extract_first()
        item['title'] = title
        #scrape thread content
        thread_contents = response.css('.wrap p::text').extract()
        item['thread_contents'] = thread_contents
        #scrape thread details
        temp = response.css('li::text').extract()
        if all(p == ' ' for p in temp):
            pass
        else:
            thread_details = temp = response.css('li::text').extract()
            item['thread_details'] = thread_details

        item['url'] = response.url
        yield item