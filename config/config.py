"""
API 配置文件
"""
import os
from enum import Enum


class Environment(Enum):
    """环境枚举"""
    PROD = "production"
    UAT = "uat"
    TEST = "test"


class Config:
    """API 配置类"""

    # 基础配置
    BASE_URL = "https://api.crypto.com/exchange/v1"
    TIMEOUT = 30
    MAX_RETRIES = 3

    # 环境配置
    CURRENT_ENV = Environment.PROD

    # 端点配置
    ENDPOINTS = {
        "candlestick": "/public/get-candlestick"
    }

    # WebSocket 配置（新增）
    WS_URL = "wss://stream.crypto.com/exchange/v1/market"
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    WS_TIMEOUT = 30
    WS_PING_INTERVAL = int(os.getenv("WS_PING_INTERVAL", "30"))
    WS_MESSAGE_TIMEOUT = 10  # WebSocket 消息接收超时

    # WebSocket 频道（新增）
    WS_CHANNELS = {"orderbook": "book.{instrument_name}.{depth}",
                   "trade": "trade.{instrument_name}",
                   "ticker": "ticker.{instrument_name}"}

    # 测试配置
    TEST_CONFIG = {
        "enable_logging": True,
        "log_level": "INFO",
        "save_response": True,
        "response_dir": "reports/responses"
    }

    # 性能基准
    PERFORMANCE_BENCHMARK = {
        "max_response_time": 2000,  # ms
        "max_response_size": 10485760,  # 10MB
    }

    @classmethod
    def get_full_url(cls, endpoint_key):
        """获取完整 URL"""
        return f"{cls.BASE_URL}{cls.ENDPOINTS[endpoint_key]}"

    @classmethod
    def get_env_config(cls):
        """获取环境配置"""
        return {
            "base_url": cls.BASE_URL,
            "timeout": cls.TIMEOUT,
            "environment": cls.CURRENT_ENV.value
        }

    @classmethod
    def get_ws_channel(cls, channel_type: str,**kwargs) -> str:
        """        获取 WebSocket 频道名称
        Args:   channel_type: 频道类型（orderbook, trade, ticker）
        **kwargs: 频道参数（如 instrument_name, depth）
        Returns:            格式化的频道名称        """
    
        channel_template = cls.WS_CHANNELS.get(channel_type, "")
        return channel_template.format(**kwargs)