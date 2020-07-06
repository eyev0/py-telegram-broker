import scrapy

from ..config import (
    GATHERER_BASE_URL,
    GATHERER_LANGUAGES_BASE_URL,
    GATHERER_SET_URL,
    LANGUAGES,
    SETS,
)
from ..items import BaseItem, LocalizedItem, Translation
from ..loaders import BaseItemLoader, LocalizationLoader, LocalizedItemLoader
from .base_spider import BaseSpider


# noinspection PyAbstractClass
class GathererSpider(BaseSpider):
    name = "gatherer"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.urls = [
            GATHERER_SET_URL.format(set_name=set_name, page=0)
            for set_url_name, set_name in SETS.items()
        ]
        self.start_page_num = 0
        self.parse_item_callback = self.parse_base_item

    def get_next_search_url(self, response, search_url, page_num):
        hyperlinks = response.css("div.pagingcontrols > div > a")
        for hyperlink in hyperlinks:
            text: str = hyperlink.css("::text").get()
            if text.find(">") > 0:
                return GATHERER_BASE_URL + hyperlink.css("::attr(href)").get()
        return ""

    def parse_base_item(self, response):
        loader = BaseItemLoader(item=BaseItem(), response=response, source=self.name)
        loader.add_attrs()
        item = loader.load_item()
        # yield base_item
        request_languages_page = scrapy.Request(
            GATHERER_LANGUAGES_BASE_URL.format(product=item["product_id"]),
            callback=self.parse_languages_page,
            cb_kwargs=dict(item=item),
        )
        yield request_languages_page

    def parse_languages_page(self, response, item):
        for selector in response.css("tr.cardItem"):
            localization_loader = LocalizationLoader(
                item=Translation(),
                selector=selector,
                response=response,
                source=self.name,
            )
            localization_loader.add_attrs()
            localization = localization_loader.load_item()
            if localization["language"] in LANGUAGES:
                request_localization = scrapy.Request(
                    localization["url"],
                    callback=self.parse_localized_item,
                    cb_kwargs=dict(item=item, language=localization["language"]),
                )
                yield request_localization

    def parse_localized_item(self, response, item, language):
        loader = LocalizedItemLoader(
            item=LocalizedItem(item.copy()), response=response, source=self.name
        )
        loader.add_attrs()
        localized_item = loader.load_item()
        yield localized_item
