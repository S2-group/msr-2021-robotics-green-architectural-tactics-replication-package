# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ROSAItem(scrapy.Item):
    # define the fields for your item here like:
    answer_details = scrapy.Field()
    question_details = scrapy.Field()
    answer = scrapy.Field()
    post_content = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()