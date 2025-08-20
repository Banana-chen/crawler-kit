import time
from crawler_kit.infrastructure.webdriver.seleniumbase_manager import (
    SeleniumBaseManager,
)
from crawler_kit.modules.general.enums.driver_config import DriverConfig
from prefect.cache_policies import NO_CACHE
from prefect import flow, get_run_logger, task
from crawler_kit.infrastructure.converts.png.to_jpg import png_to_jpg
from crawler_kit.modules.general.dtos.crawl_result import CrawlResult


class CrawlerError(Exception):
    pass


class PchomeCrawler:
    def __init__(self, request_delay: int, enable_screenshot: bool = True):
        self.request_delay = request_delay
        self.enable_screenshot = enable_screenshot

    @flow(name="crawl-pchome-page")
    def crawl_page(self, url: str) -> CrawlResult:
        logger = get_run_logger()
        logger.info(f"Start crawl page: {url}")

        result = self._fetch_page_content(url)
        logger.info(f"Successfully crawled page: {url}")
        return result

    @task(name="fetch-page-content", cache_policy=NO_CACHE)
    def _fetch_page_content(self, url: str) -> CrawlResult:
        with self._get_driver() as driver:
            driver.get(url)
            time.sleep(self.request_delay)
            content = driver.page_source
            screenshot = (
                self._take_screenshot(driver) if self.enable_screenshot else b""
            )
            return CrawlResult(url=url, content=content, screenshot=screenshot)

    @task(name="take-screenshot", cache_policy=NO_CACHE)
    def _take_screenshot(self, driver) -> bytes:
        logger = get_run_logger()
        logger.info(f"Start take screenshot")
        screenshot_data = driver.get_screenshot_as_png()
        return png_to_jpg(screenshot_data)

    def _get_driver(self):
        return SeleniumBaseManager.get_driver(**DriverConfig.Pchome.value)


if __name__ == "__main__":
    PchomeCrawler(5).crawl_page("https://24h.pchome.com.tw/prod/DBAK0X-A9006MDUL")
