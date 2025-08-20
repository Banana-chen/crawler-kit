import logging
from typing import Optional
from bs4 import BeautifulSoup
from crawler_kit.modules.general.dtos.crawl_result import ParsedProductData

logger = logging.getLogger(__name__)


class EbayParser:
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
            title = soup.title.text.strip()
            return title
        except Exception as e:
            logger.error(f"Error extracting title: {e}")
            return None

    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        price_selectors = [
            ".x-price-primary .ux-textspans",
        ]

        for selector in price_selectors:
            try:
                price_element = soup.select_one(selector)
                if price_element:
                    price = price_element.text.strip()
                    return price
            except Exception as e:
                logger.error(f"Error extracting price: {e}")
                return None

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            image_element = soup.find("meta", property="og:image")
            if image_element:
                image_url = image_element.get("content")
                return image_url
            return None
        except Exception as e:
            logger.error(f"Error extracting image: {e}")
            return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            description = soup.find("meta", property="og:description")
            if description:
                description_text = description.get("content")
                return description_text
            return None
        except Exception as e:
            logger.error(f"Error extracting description: {e}")
            return None

    def _extract_seller(self, soup: BeautifulSoup) -> Optional[str]:
        seller_selectors = [".x-sellercard-atf__info__about-seller"]
        for selector in seller_selectors:
            try:
                seller_element = soup.select_one(selector)
                if seller_element:
                    seller_name = seller_element.text.strip()
                    return seller_name
            except Exception as e:
                logger.error(f"Error extracting seller: {e}")
                return None
