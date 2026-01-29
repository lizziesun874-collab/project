"""
config/test_data/ws_data_loader.py
WebSocket 测试数据加载器
"""
from data.base_data_loader import BaseDataLoader
from data.orderbook_cases import OrderbookCases


class WebSocketDataLoader(BaseDataLoader):
    """WebSocket 测试数据加载器"""

    _CASE_TYPE_MAP = {
        "orderbook": OrderbookCases,
        # 未来扩展
        # "trade": TradeCases,
        # "ticker": TickerCases,
    }