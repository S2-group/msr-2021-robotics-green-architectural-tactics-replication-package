# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiItem(scrapy.Item):
    time = scrapy.Field()
    user = scrapy.Field()
    url = scrapy.Field()
