# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GitItem(scrapy.Item):
    # define the fields for your item here like:
    issue_title = scrapy.Field()
    issue_status = scrapy.Field()
    issue_contents = scrapy.Field()
    issue_code = scrapy.Field()
    issue_quotes = scrapy.Field()
    contents_details = scrapy.Field()
    contents_details_more = scrapy.Field()
    posted_on = scrapy.Field()
    url = scrapy.Field()
