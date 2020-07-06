from loguru import logger
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrape_magic.spiders.gatherer_spider import GathererSpider
from scrape_magic.spiders.starcity_spider import StarcitySpider


def update_items():
    settings = get_project_settings()
    process = CrawlerProcess(settings, install_root_handler=False)
    process.crawl(StarcitySpider)
    process.crawl(GathererSpider)
    try:
        process.start(stop_after_crawl=False)
    except RuntimeError as e:
        logger.error(e)
