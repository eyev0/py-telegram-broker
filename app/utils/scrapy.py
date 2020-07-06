from loguru import logger
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import DEFAULT_LOGGING
from scrapy.utils.project import get_project_settings

from scrape_magic.spiders.gatherer_spider import GathererSpider
from scrape_magic.spiders.starcity_spider import StarcitySpider

settings = get_project_settings()
DEFAULT_LOGGING["loggers"] = dict(scrapy={"level": "INFO"}, twisted={"level": "ERROR"})
process = CrawlerProcess(settings, install_root_handler=False)


def update_items():
    process.crawl(StarcitySpider)
    process.crawl(GathererSpider)
    try:
        process.start(stop_after_crawl=False)
    except RuntimeError as e:
        logger.error(e)
