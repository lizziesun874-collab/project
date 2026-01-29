"""
data/test_data.py
测试数据配置 - 使用字典结构便于维护
"""
from datetime import datetime, timedelta


class CandlestickTestData:
    """K线数据测试用例"""

    # 使用字典结构，以 case_id 为键
    POSITIVE_CASES = {
        "TC_POS_001": {
            "case_id": "TC_POS_001",
            "description": "获取 BTC 1小时 K线数据",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 100
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },
        "TC_POS_002": {
            "case_id": "TC_POS_002",
            "description": "获取 ETH 5分钟 K线（指定时间范围）",
            "params": {
                "instrument_name": "ETH_USDT",
                "timeframe": "5m",
                "start_ts": int((datetime.now() - timedelta(hours=2)).timestamp() * 1000),
                "end_ts": int(datetime.now().timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },
        "TC_POS_003": {
            "case_id": "TC_POS_003",
            "description": "获取指定数量的 K线（count=50）",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 50
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "max_data_points": 50
            }
        }
    }

    NEGATIVE_CASES = {
        "TC_NEG_001": {
            "case_id": "TC_NEG_001",
            "description": "缺少必填参数 instrument_name",
            "params": {
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400, 422],
                "has_error": True
            }
        },
        "TC_NEG_002": {
            "case_id": "TC_NEG_002",
            "description": "无效的交易对名称",
            "params": {
                "instrument_name": "INVALID_PAIR",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400, 404],
                "has_error": True
            }
        }
    }

    BOUNDARY_CASES = {
        "TC_BND_001": {
            "case_id": "TC_BND_001",
            "description": "测试最小 count=1",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 1
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "exact_count": 1
            }
        },
        "TC_BND_002": {
            "case_id": "TC_BND_002",
            "description": "测试最大 count=300",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1m",
                "count": 300
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "max_data_points": 300
            }
        }
    }

    # 提供便捷方法获取测试用例
    @classmethod
    def get_case(cls, case_id: str, case_type: str = "positive"):
        """
        根据 case_id 获取测试用例

        Args:
            case_id: 测试用例ID，如 "TC_POS_001"
            case_type: 用例类型 - "positive", "negative", "boundary"

        Returns:
            dict: 测试用例数据

        Raises:
            KeyError: 如果 case_id 不存在
        """
        case_map = {
            "positive": cls.POSITIVE_CASES,
            "negative": cls.NEGATIVE_CASES,
            "boundary": cls.BOUNDARY_CASES
        }

        cases = case_map.get(case_type.lower())
        if not cases:
            raise ValueError(f"Invalid case_type: {case_type}")

        if case_id not in cases:
            raise KeyError(f"Case ID '{case_id}' not found in {case_type} cases")

        return cases[case_id]

    @classmethod
    def get_all_cases(cls, case_type: str = "positive"):
        """
        获取某类型的所有测试用例

        Args:
            case_type: 用例类型

        Returns:
            list: 测试用例列表
        """
        case_map = {
            "positive": cls.POSITIVE_CASES,
            "negative": cls.NEGATIVE_CASES,
            "boundary": cls.BOUNDARY_CASES
        }

        cases = case_map.get(case_type.lower())
        if not cases:
            raise ValueError(f"Invalid case_type: {case_type}")

        return list(cases.values())

    @classmethod
    def get_case_ids(cls, case_type: str = "positive"):
        """
        获取某类型的所有测试用例ID

        Args:
            case_type: 用例类型

        Returns:
            list: 测试用例ID列表
        """
        case_map = {
            "positive": cls.POSITIVE_CASES,
            "negative": cls.NEGATIVE_CASES,
            "boundary": cls.BOUNDARY_CASES
        }

        cases = case_map.get(case_type.lower())
        if not cases:
            raise ValueError(f"Invalid case_type: {case_type}")

        return list(cases.keys())