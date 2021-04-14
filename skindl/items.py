# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    designer = scrapy.Field()
    preview_url = scrapy.Field()
    skin_url = scrapy.Field()
    ext = scrapy.Field()
