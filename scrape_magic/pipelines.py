# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

from itemadapter import ItemAdapter
from sqlalchemy import and_

from app.models.item import Item as db_item
from scrape_magic.config import results_dir


class ScrapeMagicPipeline:
    @classmethod
    def process_item(cls, item, spider):
        if cls.validate_item(item, spider):
            item["status"] = "error"
        return item

    @classmethod
    def validate_item(cls, item, spider):
        if spider.name == "starcity":
            if item["option_display_name"] == "Condition":
                if item["option_label"] not in [
                    "Played",
                    "Near Mint",
                    "Heavily Played",
                ]:
                    spider.logger.error("wrong item condition: %s" % item["condition"])
                    return False


class JsonWriterPipeline:
    def __init__(self):
        self._file = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self._file = open(results_dir / (spider.name + "_items.jl"), "w")

    def close_spider(self, spider):
        self._file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self._file.write(line)
        return item


class PostgresPipeline:
    def __init__(self):
        from app.models.db import db

        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @staticmethod
    async def process_item(item, spider):
        existing_item = await db_item.query.where(
            and_(
                db_item.source == item["source"],
                db_item.product_id == int(item["product_id"]),
            )
        ).gino.first()
        if not existing_item:
            await db_item.create(
                product_id=int(item["product_id"]),
                source=item["source"],
                original_name=item["name"],
                set_name=item["set_name"],
                card_type=item["card_type"],
                rarity=item["rarity"],
                finish=item["finish"],
            )
        return item
