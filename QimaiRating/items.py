# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QimairatingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()


class AppInfoItem(scrapy.Item):
    type = scrapy.Field()
    app_name = scrapy.Field()
    app_author = scrapy.Field()
    app_id = scrapy.Field()
    app_price = scrapy.Field()
    app_last_version = scrapy.Field()


class RateInfoItem(scrapy.Item):
    type = scrapy.Field()
    score_header = scrapy.Field()
    score_star = scrapy.Field()
    comment_num = scrapy.Field()


class CommentInfoItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    author_href = scrapy.Field()
    rate = scrapy.Field()
    publish_time = scrapy.Field()
    deleted = scrapy.Field()
