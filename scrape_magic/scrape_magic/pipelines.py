# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

from itemadapter import ItemAdapter


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
    def open_spider(self, spider):
        self.file = open(spider.name + "_items.jl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


# class PostgresPipeline:
#     collection_name = 'scrapy_items'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
#         return item
