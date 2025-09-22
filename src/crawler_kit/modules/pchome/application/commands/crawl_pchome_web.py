import time
from crawler_kit.infrastructure.webdriver.seleniumbase_manager import (
    SeleniumBaseManager,
)
from crawler_kit.modules.general.enums.driver_config import DriverConfig
from crawler_kit.infrastructure.converts.png.to_jpg import png_to_jpg
from crawler_kit.modules.pchome.domain.pchome_parser import PchomeParser
from adapters.documents.pchome_storage_service import PchomeStorageService
from crawler_kit.modules.general.dtos.crawl_result import CrawlResult
from prefect.cache_policies import NO_CACHE
from prefect import flow, task, get_run_logger
from crawler_kit.modules.exceptions.crawling import WebPageFetchError
from crawler_kit.modules.exceptions.parsing import ContentParseError
from crawler_kit.modules.exceptions.storage import DocumentStorageError




class PchomeWebCrawler:
    def __init__(self, request_delay: int, trace_id: str):
        self.request_delay = request_delay
        self.trace_id = trace_id
        self.enable_screenshot = enable_screenshot
        self.parser = PchomeParser()
        self.storage = PchomeStorageService()

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

        except (WebPageFetchError, ContentParseError, DocumentStorageError) as e:
            logger.error(f"Error processing URL {url}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error processing URL {url}: {e}")
            raise e

    @task(name="crawl-and-parse", cache_policy=NO_CACHE)
    def _crawl_and_parse(self, url: str, parse_content: bool = True) -> CrawlResult:
        logger = get_run_logger()
        logger.info(f"Crawling content from: {url}")
        
        with self._get_driver() as driver:
            driver.get(url)
            time.sleep(self.request_delay)
            content = driver.page_source
            screenshot = (
                self._take_screenshot(driver) if self.enable_screenshot else b""
            )

        parsed_data = None
        if parse_content:
            logger.info(f"Parsing content for: {url}")
            parsed_data = self.parser.parse_product_page(content)
            if not parsed_data:
                raise ContentParseError("Failed to parse page content")

        return CrawlResult(
            url=url,
            content=content,
            parsed_data=parsed_data,
            screenshot=screenshot,
        )
        
    @task(name="take-screenshot", cache_policy=NO_CACHE)
    def _take_screenshot(self, driver) -> bytes:
        logger = get_run_logger()
        logger.info("Taking screenshot")
        screenshot_data = driver.get_screenshot_as_png()
        return png_to_jpg(screenshot_data)

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

        except DocumentStorageError as e:
            logger.error(f"Error saving crawl result for URL {crawl_data.url}: {e}")
            raise DocumentStorageError(f"Failed to save crawl result for URL: {crawl_data.url}")

    def _get_driver(self):
        return SeleniumBaseManager.get_driver(**DriverConfig.Pchome.value)