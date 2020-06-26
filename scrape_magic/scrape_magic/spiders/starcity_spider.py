import json

import scrapy

from ..items import (
    ScrapedItem,
    ScrapedItemLoader,
    ScrapedItemVariant,
    ScrapedItemVariantLoader,
)


# noinspection PyAbstractClass
class StarcitySpider(scrapy.Spider):
    name = "starcity"

    base_url = "https://starcitygames.com/shop/singles/english/{set_name}/?limit=100"
    variants_base_url = (
        "https://newstarcityconnector.herokuapp.com/eyApi/"
        "products/{product}/variants"
    )

    def start_requests(self):
        sets = [
            "game-night-2019",
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
