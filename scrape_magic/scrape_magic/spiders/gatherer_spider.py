import scrapy

from ..items import BaseItem, TranslatedItem, Translation, URLList
from ..loaders import (
    BaseItemLoader,
    TranslatedItemLoader,
    TranslationLoader,
    URLListLoader,
)
from .base_spider import BaseSpider
from .config import GATHERER_LANGUAGES_BASE_URL, GATHERER_SET_URL, LANGUAGES, SETS


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

    def parse_base_item(self, response):
        loader = BaseItemLoader(item=BaseItem(), response=response, source=self.name)
        loader.add_attrs()
        base_item = loader.load_item()
        # yield base_item
        request_translations_page = scrapy.Request(
            GATHERER_LANGUAGES_BASE_URL.format(product=base_item["product_id"]),
            callback=self.parse_translations_page,
            cb_kwargs=dict(base_item=base_item),
        )
        yield request_translations_page

    def parse_translations_page(self, response, base_item):
        for transaltion_selector in response.css("tr.cardItem"):
            translation_loader = TranslationLoader(
                item=Translation(),
                selector=transaltion_selector,
                response=response,
                source=self.name,
            )
            translation_loader.add_attrs()
            translation = translation_loader.load_item()
            if translation["language"] in LANGUAGES:
                request_translation = scrapy.Request(
                    translation["url"],
                    callback=self.parse_translated_item,
                    cb_kwargs=dict(
                        base_item=base_item, language=translation["language"]
                    ),
                )
                yield request_translation

    def parse_translated_item(self, response, base_item, language):
        loader = TranslatedItemLoader(
            item=TranslatedItem(base_item.copy()), response=response, source=self.name
        )
        loader.add_attrs()
        translated_item = loader.load_item()
        yield translated_item
