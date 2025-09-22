class CrawlBaseError(Exception):
    """所有爬蟲異常的基類"""
    pass

class DriverInitError(CrawlBaseError):
    """Driver 初始化失敗"""
    pass

class WebPageFetchError(CrawlBaseError):
    """網頁抓取失敗"""
    pass

class PageTimeoutError(WebPageFetchError):
    """頁面載入超時 - 需要調整等待時間或重試"""
    pass

class PageNotFoundError(WebPageFetchError):
    """頁面不存在 (404) - 不應重試"""
    pass

    