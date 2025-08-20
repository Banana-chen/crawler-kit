from typing import NamedTuple, Optional


class ParsedProductData(NamedTuple):
    title: Optional[str] = None
    description: Optional[str] = None
    seller: Optional[str] = None
    price: Optional[str] = None
    thumbnail: Optional[str] = None


class CrawlResult(NamedTuple):
    url: str
    content: str
    screenshot: Optional[bytes] = None
    parsed_data: Optional[ParsedProductData] = None

    @classmethod
    def from_raw_crawl(cls, url: str, content: str, screenshot: Optional[bytes] = None):
        return cls(url=url, content=content, screenshot=screenshot)

    def with_parsed_data(self, parsed_data: ParsedProductData) -> "CrawlResult":
        return self._replace(parsed_data=parsed_data)
