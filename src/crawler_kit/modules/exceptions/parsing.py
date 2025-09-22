class ContentParseError(Exception):
    """
    內容解析失敗 - 通常表示網站結構變更
    
    處理策略：
    - 通知開發者更新解析規則
    - 記錄失敗案例供調試
    - 不建議自動重試
    """
    pass


class ParserNotFoundError(ContentParseError):
    """找不到適合的解析器 - 配置問題"""
    pass


class RequiredFieldMissingError(ContentParseError):
    """必要欄位解析失敗 - HTML 結構可能變更"""
    pass
