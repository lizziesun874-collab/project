"""
config/test_data/base_data_loader.py
测试数据加载器基类
"""
from typing import Dict, List, Any, Type


class BaseDataLoader:
    """测试数据加载器基类"""

    _CASE_TYPE_MAP: Dict[str, Type] = {}

    @classmethod
    def get_case(cls, case_id: str, case_type: str) -> Dict[str, Any]:
        """获取测试用例"""
        case_type = case_type.lower()

        if case_type not in cls._CASE_TYPE_MAP:
            raise ValueError(f"Invalid case_type: '{case_type}'")

        cases = cls._CASE_TYPE_MAP[case_type].CASES

        if case_id not in cases:
            raise KeyError(f"Case ID '{case_id}' not found")

        return cases[case_id].copy()

    @classmethod
    def get_all_cases(cls, case_type: str) -> List[Dict[str, Any]]:
        """获取所有测试用例"""
        case_type = case_type.lower()

        if case_type not in cls._CASE_TYPE_MAP:
            raise ValueError(f"Invalid case_type: '{case_type}'")

        cases = cls._CASE_TYPE_MAP[case_type].CASES
        return [case.copy() for case in cases.values()]

    @classmethod
    def get_case_ids(cls, case_type: str) -> List[str]:
        """获取所有测试用例ID"""
        case_type = case_type.lower()

        if case_type not in cls._CASE_TYPE_MAP:
            raise ValueError(f"Invalid case_type: '{case_type}'")

        return list(cls._CASE_TYPE_MAP[case_type].CASES.keys())

    @classmethod
    def get_cases_by_tag(cls, tag: str, case_type: str) -> List[Dict[str, Any]]:
        """根据标签获取测试用例"""
        all_cases = cls.get_all_cases(case_type)
        return [case for case in all_cases if tag in case.get("tags", [])]

    @classmethod
    def get_cases_by_priority(cls, priority: str, case_type: str) -> List[Dict[str, Any]]:
        """根据优先级获取测试用例"""
        all_cases = cls.get_all_cases(case_type)
        return [case for case in all_cases if case.get("priority") == priority]

    @classmethod
    def get_smoke_cases(cls, case_type: str) -> List[Dict[str, Any]]:
        """获取冒烟测试用例"""
        return cls.get_cases_by_tag("smoke", case_type)