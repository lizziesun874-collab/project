"""
config/test_data/rest_data_loader.py
REST API 测试数据加载器
"""
from data import PositiveCases, NegativeCases, BoundaryCases, PerformanceCases
from data.base_data_loader import BaseDataLoader



class RestDataLoader(BaseDataLoader):
    """REST API 测试数据加载器"""

    _CASE_TYPE_MAP = {
        "positive": PositiveCases,
        "negative": NegativeCases,
        "boundary": BoundaryCases,
        "performance": PerformanceCases
    }