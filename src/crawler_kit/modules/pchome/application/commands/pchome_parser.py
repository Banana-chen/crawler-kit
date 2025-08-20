import logging
from typing import Optional
from bs4 import BeautifulSoup
from crawler_kit.modules.general.dtos.crawl_result import ParsedProductData

logger = logging.getLogger(__name__)


class PchomeParser:
    def parse_product_page(self, content: str) -> Optional[ParsedProductData]:
        soup = BeautifulSoup(content, "html.parser")

        return ParsedProductData(
            title=self._extract_title(soup),
            price=self._extract_price(soup),
            thumbnail=self._extract_image(soup),
            description=self._extract_description(soup),
            seller=self._extract_seller(soup),
        )

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            if soup.title:
                title = soup.title.text.strip()
                if " - " in title:
                    title = title.split(" - ")[0]
                return title if title else None

            h1 = soup.find("h1")
            if h1:
                return h1.get_text(strip=True)

            return None
        except Exception as e:
            logger.error(f"Error extracting title: {e}")
            return None

    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            price_selectors = [
                ".price",
                ".product-price",
                "[class*='price']",
                ".sale-price",
                ".current-price",
            ]

            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    if price_text:
                        return price_text

            return None
        except Exception as e:
            logger.error(f"Error extracting price: {e}")
            return None

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                return og_image.get("content")

            img_selectors = [
                ".product-image img",
                ".main-image img",
                "[class*='product'] img[src]",
            ]

            for selector in img_selectors:
                img = soup.select_one(selector)
                if img and img.get("src"):
                    return img.get("src")

            return None
        except Exception as e:
            logger.error(f"Error extracting image: {e}")
            return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            og_desc = soup.find("meta", property="og:description")
            if og_desc and og_desc.get("content"):
                return og_desc.get("content")

            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                return meta_desc.get("content")

            desc_selectors = [".product-description", ".description", "[class*='desc']"]

            for selector in desc_selectors:
                desc = soup.select_one(selector)
                if desc:
                    desc_text = desc.get_text(strip=True)
                    if desc_text and len(desc_text) > 10:
                        return desc_text

            return None
        except Exception as e:
            logger.error(f"Error extracting description: {e}")
            return None

    def _extract_seller(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            seller_selectors = [
                ".seller",
                ".seller-name",
                ".store-name",
                "[class*='seller']",
                "[class*='store']",
            ]

            for selector in seller_selectors:
                seller_elem = soup.select_one(selector)
                if seller_elem:
                    seller_text = seller_elem.get_text(strip=True)
                    if seller_text:
                        return seller_text

            return None
        except Exception as e:
            logger.error(f"Error extracting seller: {e}")
            return None
