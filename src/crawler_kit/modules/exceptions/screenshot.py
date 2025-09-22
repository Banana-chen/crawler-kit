class ScreenshotCaptureError(Exception):
    """
    截圖失敗 - 通常是瀏覽器或轉換問題
    
    處理策略：
    - 可以跳過截圖繼續其他處理
    - 檢查瀏覽器狀態
    - 驗證圖片轉換邏輯
    """
    pass


class ImageConvertError(ScreenshotCaptureError):
    """圖片格式轉換失敗"""
    pass
