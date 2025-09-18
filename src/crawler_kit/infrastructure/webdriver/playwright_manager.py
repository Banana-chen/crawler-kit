from playwright.async_api import async_playwright, Browser, Page, Playwright
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
import logging
import time
import asyncio


logger = logging.getLogger(__name__)


class PlaywrightManager:
    
    @classmethod
    @asynccontextmanager
    async def get_page(
        cls,
        browser: str = "chromium",
        headless: bool = False,
        use_system_browser: bool = False,
        window_size: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[Page, None]:
        start_time = time.time()
        
        if use_system_browser and browser == "chromium":
            kwargs["executable_path"] = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        async with async_playwright() as p:
            browser_instance = await getattr(p, browser).launch(headless=headless, **kwargs)
            
            page_options = {}
            if window_size:
                w, h = map(int, window_size.split(','))
                page_options['viewport'] = {'width': w, 'height': h}
            
            page = await browser_instance.new_page(**page_options)
            
            logger.info(f"Browser ready in {time.time() - start_time:.2f}s")
            
            try:
                yield page
            finally:
                await browser_instance.close()

    @classmethod
    @asynccontextmanager
    async def get_browser(
        cls,
        browser: str = "chromium", 
        headless: bool = False,
        use_system_browser: bool = False,
        **kwargs
    ) -> AsyncGenerator[Browser, None]:
        start_time = time.time()
        
        if use_system_browser and browser == "chromium":
            kwargs["executable_path"] = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        async with async_playwright() as p:
            browser_instance = await getattr(p, browser).launch(headless=headless, **kwargs)
            
            logger.info(f"Browser ready in {time.time() - start_time:.2f}s")
            
            try:
                yield browser_instance
            finally:
                await browser_instance.close()


async def main():
    async with PlaywrightManager.get_page(
        browser="chromium",
        headless=False,
        use_system_browser=True,
        window_size="1920,1080"
    ) as page:
        await page.goto("https://medium.com/@mkaanaslan99/time-series-forecasting-with-a-basic-transformer-model-in-pytorch-650f116a1018")
        state = await page.context.storage_state()
        print(state)
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())