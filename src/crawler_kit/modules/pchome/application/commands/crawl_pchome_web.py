from crawler_kit.modules.pchome.application.commands.pchome_crawler import PchomeCrawler
from crawler_kit.modules.pchome.application.commands.pchome_parser import PchomeParser
from crawler_kit.modules.pchome.application.commands.pchome_storage_service import (
    PchomeStorageService,
    StorageError,
)
from crawler_kit.modules.general.dtos.crawl_result import CrawlResult
from prefect.cache_policies import NO_CACHE
from prefect import flow, task, get_run_logger


class CrawlerError(Exception):
    pass


class PchomeWebCrawler:
    def __init__(self, request_delay: int, trace_id: str):
        self.crawler = PchomeCrawler(request_delay)
        self.parser = PchomeParser()
        self.storage = PchomeStorageService()
        self.trace_id = trace_id

    @flow(name="crawl-pchome-web")
    def __call__(
        self, url: str, skip_if_exists: bool = False, parse_content: bool = True
    ) -> CrawlResult:
        logger = get_run_logger()
        logger.info(f"Processing URL: {url}")
        try:
            if skip_if_exists:
                existing_hash = self.storage.check_url_exists(url)
                if existing_hash:
                    logger.info(f"URL already exists, skipping: {url}")
                    return CrawlResult(url=url, content="")

            result = self._crawl_and_parse(url, parse_content)
            self._save_result(result)
            logger.info(f"Successfully processed URL: {url}")
            return result

        except (CrawlerError, StorageError) as e:
            logger.error(f"Error processing URL {url}: {e}")
            return CrawlResult(url=url, content="")
        except Exception as e:
            logger.error(f"Unexpected error processing URL {url}: {e}")
            return CrawlResult(url=url, content="")

    @task(name="crawl-and-parse", cache_policy=NO_CACHE)
    def _crawl_and_parse(self, url: str, parse_content: bool = True) -> CrawlResult:
        logger = get_run_logger()
        logger.info(f"Crawling content from: {url}")

        crawl_result = self.crawler.crawl_page(url)
        if not crawl_result:
            raise CrawlerError(f"Failed to crawl content from URL: {url}")

        parsed_data = None
        if parse_content:
            logger.info(f"Parsing content for: {url}")
            parsed_data = self.parser.parse_product_page(crawl_result.content)
            if not parsed_data:
                raise CrawlerError("Failed to parse page content")

        return CrawlResult(
            url=url,
            content=crawl_result.content,
            parsed_data=parsed_data,
            screenshot=crawl_result.screenshot,
        )

    @task(name="save-crawl-result", cache_policy=NO_CACHE)
    def _save_result(self, crawl_data: CrawlResult) -> None:
        logger = get_run_logger()
        logger.info(f"Saving crawl result for URL: {crawl_data.url}")
        try:
            self.storage.save_crawled_data(
                self.trace_id,
                crawl_data.url,
                crawl_data.content,
                parsed_data=crawl_data.parsed_data,
                screenshot=crawl_data.screenshot,
            )

        except StorageError as e:
            logger.error(f"Error saving crawl result for URL {crawl_data.url}: {e}")
            raise CrawlerError(f"Failed to save crawl result for URL: {crawl_data.url}")
