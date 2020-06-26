import json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class StarcitySpider(scrapy.Spider):
    name = "starcity"

    base_url = "https://starcitygames.com/shop/singles/english/{set_name}/?limit=100"
    variants_base_url = (
        "https://newstarcityconnector.herokuapp.com/eyApi/"
        "products/{product}/variants"
    )

    def start_requests(self):
        sets = [
            "welcome-deck-2016",
            # "core-set-2021",
            # "core-set-2020",
        ]
        urls = [self.base_url.format(set_name=set_name) for set_name in sets]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page,
                cb_kwargs=dict(main_url=url, page_num=1),
            )

    def parse_page(self, response, main_url, page_num):
        for product in response.css("tr.product"):
            item_url = product.css(
                "div.listItem-details > h4.listItem-title > a::attr(href)"
            ).get()
            request_item = scrapy.Request(item_url, callback=self.parse_item,)
            yield request_item

        if response.status != 404:
            page_num += 1
            next_url = main_url + f"&page={page_num}"
            request_next_page = scrapy.Request(
                next_url,
                callback=self.parse_page,
                cb_kwargs=dict(main_url=main_url, page_num=page_num),
            )
            yield request_next_page

    def parse_item(self, response):
        loader = ScrapedItemLoader(item=ScrapedItem(), response=response)
        item = loader.load_item()
        request_variants = scrapy.Request(
            self.variants_base_url.format(product=item["product_id"]),
            callback=self.parse_item_variants,
            cb_kwargs=dict(item=item),
        )
        yield request_variants

    @staticmethod
    def parse_item_variants(response, item):
        response_data = json.loads(response.text)["response"]["data"]
        for data in response_data:
            for option in data["option_values"]:
                loader = ScrapedItemVariantLoader(
                    variant_data=data,
                    option=option,
                    item=ScrapedItemVariant(item.copy()),
                )
                yield loader.load_item()


class ScrapedItem(scrapy.Item):
    status = scrapy.Field()
    product_id = scrapy.Field(serializer=int)
    name = scrapy.Field()
    img_src = scrapy.Field()
    card_type = scrapy.Field()
    set = scrapy.Field()
    rarity = scrapy.Field()
    finish = scrapy.Field()


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
            re="([^\t\n\r\f\v']+)\\r",
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
            "dd.productView-info-value[data-field='Finish']::text",
            re="([^\t\n\r\f\v']+)\\r",
        )


class ScrapedItemVariant(ScrapedItem):
    variant_id = scrapy.Field(serializer=int)
    price = scrapy.Field(serializer=float)
    calculated_price = scrapy.Field(serializer=float)
    option_display_name = scrapy.Field()
    option_label = scrapy.Field()


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
