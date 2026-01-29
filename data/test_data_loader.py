"""
data/test_data_loader.py
测试数据加载器 - 统一入口（向后兼容）
"""
from typing import Dict, List, Any
from data.rest_data_loader import RestDataLoader
from data.ws_data_loader import WebSocketDataLoader


class TestDataLoader:
    """测试数据加载器 - 统一访问入口"""

    # 子加载器
    rest = RestDataLoader
    ws = WebSocketDataLoader
    websocket = WebSocketDataLoader

    # ========== 向后兼容方法（保持原有调用方式）==========

    @classmethod
    def get_case(cls, case_id: str, case_type: str = "positive") -> Dict[str, Any]:
        """获取测试用例（默认 REST API）"""
        return cls.rest.get_case(case_id, case_type)

    @classmethod
    def get_all_cases(cls, case_type: str = "positive") -> List[Dict[str, Any]]:
        """获取所有测试用例（默认 REST API）"""
        return cls.rest.get_all_cases(case_type)

    @classmethod
    def get_case_ids(cls, case_type: str = "positive") -> List[str]:
        """获取所有测试用例ID（默认 REST API）"""
        return cls.rest.get_case_ids(case_type)

    @classmethod
    def get_cases_by_tag(cls, tag: str, case_type: str = "positive") -> List[Dict[str, Any]]:
        """根据标签获取测试用例（默认 REST API）"""
        return cls.rest.get_cases_by_tag(tag, case_type)

    @classmethod
    def get_cases_by_priority(cls, priority: str, case_type: str = "positive") -> List[Dict[str, Any]]:
        """根据优先级获取测试用例（默认 REST API）"""
        return cls.rest.get_cases_by_priority(priority, case_type)

    @classmethod
    def get_smoke_cases(cls, case_type: str = "positive") -> List[Dict[str, Any]]:
        """获取冒烟测试用例（默认 REST API）"""
        return cls.rest.get_smoke_cases(case_type)


# 便捷访问类
class CandlestickTestData:
    """K线数据测试用例 - 便捷访问接口"""

    @staticmethod
    def get_case(case_id: str, case_type: str = "positive") -> Dict[str, Any]:
        """获取测试用例"""
        return TestDataLoader.get_case(case_id, case_type)

    @staticmethod
    def get_all_cases(case_type: str = "positive") -> List[Dict[str, Any]]:
        """获取所有测试用例"""
        return TestDataLoader.get_all_cases(case_type)

    @staticmethod
    def get_case_ids(case_type: str = "positive") -> List[str]:
        """获取所有测试用例ID"""
        return TestDataLoader.get_case_ids(case_type)


# 创建全局实例
test_data_loader = TestDataLoader()