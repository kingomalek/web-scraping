# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelscomItem(scrapy.Item):
	titre = scrapy.Field()
	price = scrapy.Field()
	review = scrapy.Field()
	city = scrapy.Field()
	country = scrapy.Field()
	host = scrapy.Field()
	timestamp = scrapy.Field()
	idx = scrapy.Field()
	stars = scrapy.Field()
	el_id = scrapy.Field()

