# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GitItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    username_url = scrapy.Field()
    pr_title = scrapy.Field()
    pr_status = scrapy.Field()
    pr_contents = scrapy.Field()
    pr_code = scrapy.Field()
    pr_quotes = scrapy.Field()
    contents_details = scrapy.Field()
    contents_details_more = scrapy.Field()
    posted_on = scrapy.Field()
    url = scrapy.Field()
