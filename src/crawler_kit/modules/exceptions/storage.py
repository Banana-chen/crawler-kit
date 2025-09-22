class DocumentStorageError(Exception):
    """
    文檔存儲失敗 - 資料庫或檔案系統問題
    
    處理策略：
    - 嘗試備用存儲方式
    - 記錄到本地檔案
    - 檢查權限和連線狀態
    """
    pass


class StorageConnectionError(DocumentStorageError):
    """存儲系統連線失敗 - 網路或認證問題"""
    pass


class StorageQuotaExceededError(DocumentStorageError):
    """存儲配額超限 - 需要清理或擴容"""
    pass
