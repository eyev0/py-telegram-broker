# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapeMagicPipeline:
    @classmethod
    def process_item(cls, item, spider):
        if cls.validate_item(item, spider):
            item["status"] = "error"
        return item

    @classmethod
    def validate_item(cls, item, spider):
        if item["option_display_name"] == "Condition":
            if item["option_label"] not in ["Played", "Near Mint", "Heavily Played"]:
                spider.logger.error("wrong item condition: %s" % item["condition"])
                return False
