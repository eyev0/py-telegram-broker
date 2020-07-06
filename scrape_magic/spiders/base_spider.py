from abc import abstractmethod

import scrapy

from ..items import URLList
from ..loaders import URLListLoader


# noinspection PyAbstractClass
class BaseSpider(scrapy.Spider):
    __abstract__ = True
    name = "base"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.urls = None
        self.start_page_num = 0

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_set_page,
                cb_kwargs=dict(search_url=url, page_num=self.start_page_num),
            )

    @abstractmethod
    def parse_item_callback(self, response):
        raise NotImplementedError

    @abstractmethod
    def get_next_search_url(self, response, search_url, page_num):
        raise NotImplementedError

    def parse_set_page(self, response, search_url, page_num):
        url_loader = URLListLoader(item=URLList(), response=response, source=self.name)
        urls = url_loader.load_item().get("urls", [])
        for item_url in urls:
            request_item = scrapy.Request(item_url, callback=self.parse_item_callback,)
            yield request_item

        if next_page_url := self.get_next_search_url(
            response, search_url, page_num := page_num + 1
        ):
            request_next_page = scrapy.Request(
                next_page_url,
                callback=self.parse_set_page,
                cb_kwargs=dict(search_url=search_url, page_num=page_num),
            )
            yield request_next_page
