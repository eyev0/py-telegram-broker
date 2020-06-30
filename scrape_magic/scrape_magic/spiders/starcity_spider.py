import json

import scrapy

from ..config import SETS, STARCITY_CARD_VARIANTS_URL, STARCITY_SET_URL
from ..items import BaseItem, PricedItem
from ..loaders import BaseItemLoader, PricedItemLoader
from .base_spider import BaseSpider


# noinspection PyAbstractClass
class StarcitySpider(BaseSpider):
    name = "starcity"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.urls = [
            STARCITY_SET_URL.format(set_url_name=set_url_name, page=1)
            for set_url_name, _ in SETS.items()
        ]
        self.start_page_num = 1
        self.parse_item_callback = self.parse_base_item

    @classmethod
    def parse_base_item(cls, response):
        loader = BaseItemLoader(item=BaseItem(), response=response, source=cls.name)
        loader.add_attrs()
        base_item = loader.load_item()
        request_variants = scrapy.Request(
            STARCITY_CARD_VARIANTS_URL.format(product=base_item["product_id"]),
            callback=cls.parse_priced_item,
            cb_kwargs=dict(base_item=base_item),
        )
        yield request_variants

    @staticmethod
    def parse_priced_item(response, base_item):
        response_data = json.loads(response.text)["response"]["data"]
        for data in response_data:
            for option in data["option_values"]:
                loader = PricedItemLoader(
                    item=PricedItem(base_item.copy()), response=response
                )
                loader.add_attrs(data, option)
                yield loader.load_item()
