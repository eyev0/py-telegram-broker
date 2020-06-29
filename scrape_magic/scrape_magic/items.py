# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ScrapedItem(scrapy.Item):
    status = scrapy.Field()
    product_id = scrapy.Field(serializer=int)
    name = scrapy.Field()
    img_src = scrapy.Field()
    card_type = scrapy.Field()
    set = scrapy.Field()
    rarity = scrapy.Field()
    finish = scrapy.Field()


class ScrapedItemVariant(ScrapedItem):
    variant_id = scrapy.Field(serializer=int)
    price = scrapy.Field(serializer=float)
    calculated_price = scrapy.Field(serializer=float)
    option_display_name = scrapy.Field()
    option_label = scrapy.Field()


class ScrapedItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_value("status", "ok")
        self.add_css("product_id", "div.productView-product::attr(value)")
        # re = trim single quotes and whitespace characters (except for spaces)
        self.add_css(
            "name",
            "dd.productView-info-value[data-field='Card Name']::text",
            re="([^\t\n\r\f\v]+)\\r",
        )
        self.add_css(
            "img_src", "img.productView-image--default::attr(data-src)",
        )
        self.add_css(
            "card_type",
            "dd.productView-info-value[data-field='Card Type']::text",
            re="([^\t\n\r\f\v']+)\\r",
        )
        self.add_css(
            "set",
            "dd.productView-info-value[data-field='Set']::text",
            re="([^\t\n\r\f\v']+)\\r",
        )
        self.add_css(
            "finish",
            "dd.productView-info-value[data-field='Finish']::text",
            re="([^\t\n\r\f\v']+)\\r",
        )
        self.add_css(
            "rarity",
            "dd.productView-info-value[data-field='Rarity']::text",
            re="([^\t\n\r\f\v']+)\\r",
        )


class ScrapedItemVariantLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def __init__(self, variant_data=None, option=None, **kwargs):
        super().__init__(**kwargs)
        self.add_value("variant_id", variant_data["id"])
        self.add_value("price", variant_data["price"])
        self.add_value("calculated_price", variant_data["calculated_price"])
        self.add_value("option_display_name", option["option_display_name"])
        self.add_value("option_label", option["label"])

        self.add_value("status", "ok")
