"""
data/__init__.py
统一导出测试数据接口
"""

# 1. 先导入测试用例类（底层，无依赖）
from data.positive_cases import PositiveCases
from data.negative_cases import NegativeCases
from data.boundary_cases import BoundaryCases
from data.performance_cases import PerformanceCases
from data.orderbook_cases import OrderbookCases

# 2. 导入基类（依赖测试用例类）
from data.base_data_loader import BaseDataLoader

# 3. 导入具体加载器（依赖基类和测试用例类）
from data.rest_data_loader import RestDataLoader
from data.ws_data_loader import WebSocketDataLoader

# 4. 导入统一入口（依赖具体加载器）
from data.test_data_loader import TestDataLoader, CandlestickTestData, test_data_loader

__all__ = [
    # ========== 主要接口（推荐使用）==========
    'TestDataLoader',  # 统一入口
    'test_data_loader',  # 全局实例
    'CandlestickTestData',  # 便捷访问类

    # ========== 子加载器 ==========
    'RestDataLoader',  # REST API 加载器
    'WebSocketDataLoader',  # WebSocket 加载器
    'BaseDataLoader',  # 基类（高级用法）

    # ========== 测试用例类（直接访问原始数据）==========
    'PositiveCases',
    'NegativeCases',
    'BoundaryCases',
    'PerformanceCases',
    'OrderbookCases',
]