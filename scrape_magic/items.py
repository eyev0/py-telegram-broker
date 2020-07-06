# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose

from .config import GATHERER_BASE_URL


def complete_item_url(url: str, loader_context):
    source = loader_context.get("source", "")
    if source == "gatherer":
        url = GATHERER_BASE_URL + url.replace("../", "/Pages/")
    return url


def complete_image_url(url: str, loader_context):
    source = loader_context.get("source", "")
    if source == "gatherer":
        url = GATHERER_BASE_URL + url.replace("../../", "/")
    return url


def complete_translation_url(url: str, loader_context):
    source = loader_context.get("source", "")
    if source == "gatherer":
        url = GATHERER_BASE_URL + "/Pages/Card/" + url
    return url


class URLList(scrapy.Item):
    urls = scrapy.Field(input_processor=MapCompose(complete_item_url))


class Translation(scrapy.Item):
    language = scrapy.Field()
    url = scrapy.Field(input_processor=MapCompose(complete_translation_url))


class BaseItem(scrapy.Item):
    status = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    product_id = scrapy.Field(serializer=int)
    name = scrapy.Field()
    image_url = scrapy.Field(input_processor=MapCompose(complete_image_url))
    card_type = scrapy.Field()
    set_name = scrapy.Field()
    rarity = scrapy.Field()
    finish = scrapy.Field()


class LocalizedItem(BaseItem):
    translated_source_url = scrapy.Field()
    translated_product_id = scrapy.Field()
    translated_image_url = scrapy.Field(input_processor=MapCompose(complete_image_url))
    translated_name = scrapy.Field()


class ItemOption(BaseItem):
    variant_id = scrapy.Field(serializer=int)
    price = scrapy.Field(serializer=float)
    calculated_price = scrapy.Field(serializer=float)
    option_display_name = scrapy.Field()
    option_label = scrapy.Field()
