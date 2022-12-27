# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class zimItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Master_BL = scrapy.Field()
    container = scrapy.Field()
    last_activity = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    voyage = scrapy.Field()
    pass
