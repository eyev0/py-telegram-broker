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
        self.parse_item_callback = None

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_set_page,
                cb_kwargs=dict(main_url=url, page_num=self.start_page_num),
            )

    def parse_set_page(self, response, main_url, page_num):
        url_loader = URLListLoader(item=URLList(), response=response, source=self.name)
        urls = url_loader.load_item().get("urls", [])
        for item_url in urls:
            request_item = scrapy.Request(item_url, callback=self.parse_item_callback,)
            yield request_item

        if response.status != 404 and len(urls) > 0:
            page_num += 1
            next_page_url = main_url + f"&page={page_num}"
            request_next_page = scrapy.Request(
                next_page_url,
                callback=self.parse_set_page,
                cb_kwargs=dict(main_url=main_url, page_num=page_num),
            )
            yield request_next_page
