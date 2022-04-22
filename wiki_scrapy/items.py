# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class WikiScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    caption = scrapy.Field()
    data = scrapy.Field()
    short_desc = scrapy.Field()
