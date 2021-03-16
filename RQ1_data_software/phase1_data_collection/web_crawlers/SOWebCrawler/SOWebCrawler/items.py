# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SOItem(scrapy.Item):
    # define the fields for your item here like:
    quote = scrapy.Field()
    question_code = scrapy.Field()
    answer_code = scrapy.Field()
    answer = scrapy.Field()
    post_content = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
