# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiItem(scrapy.Item):
    # define the fields for your item here like:
    package = scrapy.Field()
    package_summary = scrapy.Field()
    package_code = scrapy.Field()
    package_tt = scrapy.Field()
    package_details = scrapy.Field()
    url = scrapy.Field()
