from scrapy.loader import Identity, ItemLoader
from scrapy.loader.processors import TakeFirst


class URLListLoader(ItemLoader):
    default_output_processor = Identity()

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        super().__init__(item, selector, response, parent, **context)

        # starcity item
        self.add_css("urls", "div.listItem-details > h4.listItem-title > a::attr(href)")
        # gatherer item
        self.add_css("urls", "tr.cardItem > td > a::attr(href)")


class TranslationLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def add_attrs(self):
        self.add_css("url", "td.fullWidth > a::attr(href)")
        self.add_css("language", "td.fullWidth + td::text", re=r"\r\n\s+(.+)\r\n")


class BaseItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        super().__init__(item, selector, response, parent, **context)

        source = context.get("source", "")
        self.add_value("source", source)
        self.add_value("status", "ok")
        self.add_value("url", response.url)
        self.response_url = response.url
        self.source = source

    def add_attrs(self):
        if self.source == "starcity":
            self.load_from_starcity()
        elif self.source == "gatherer":
            self.load_from_gatherer()

    def load_from_starcity(self):
        self.add_css(
            "set",
            "dd.productView-info-value[data-field='Set']::text",
            re=r"([^\t\n\r\f\v']+)\r",
        )
        self.add_css(
            "name",
            "dd.productView-info-value[data-field='Card Name']::text",
            re=r"([^\t\n\r\f\v]+)\r",
        )
        self.add_css("product_id", "div.productView-product::attr(value)")
        self.add_css(
            "img_src", "img.productView-image--default::attr(data-src)",
        )
        self.add_css(
            "card_type",
            "dd.productView-info-value[data-field='Card Type']::text",
            re=r"([^\t\n\r\f\v']+)\r",
        )
        self.add_css(
            "finish",
            "dd.productView-info-value[data-field='Finish']::text",
            re=r"([^\t\n\r\f\v']+)\r",
        )
        self.add_css(
            "rarity",
            "dd.productView-info-value[data-field='Rarity']::text",
            re=r"([^\t\n\r\f\v']+)\r",
        )

    def load_from_gatherer(self):
        self.add_css(
            "set",
            "div#ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"
            " > a ~ a::text",
            re=r"([^\t\n\r\f\v]+)",
        )
        self.add_css(
            "name", "div.cardImage > img::attr(alt)",
        )
        self.add_value("product_id", self.response_url, re=r"multiverseid=(\d+)")
        self.add_css(
            "img_src", "div.cardImage > img::attr(src)",
        )
        self.add_css(
            "card_type",
            "div#ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow"
            " > div.value::text",
            re=r"\r\n\s+([^\t\n\r\f\v]+)",
        )
        self.add_value(
            "finish", "",
        )
        self.add_css(
            "rarity",
            "div#ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"
            " > div.value > span::text",
            re=r"([^\t\n\r\f\v]+)",
        )


class PricedItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def add_attrs(self, variant_data, option):
        self.add_value("variant_id", variant_data["id"])
        self.add_value("price", variant_data["price"])
        self.add_value("calculated_price", variant_data["calculated_price"])
        self.add_value("option_display_name", option["option_display_name"])
        self.add_value("option_label", option["label"])


class TranslatedItemLoader(BaseItemLoader):
    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        super().__init__(item, selector, response, parent, **context)
        self.add_value("translated_url", response.url)

    def add_attrs(self):
        self.add_css(
            "translated_name", "div.cardImage > img::attr(alt)",
        )
        self.add_value(
            "translated_product_id", self.response_url, re=r"multiverseid=(\d+)"
        )
        self.add_css(
            "translated_img_src", "div.cardImage > img::attr(src)",
        )
