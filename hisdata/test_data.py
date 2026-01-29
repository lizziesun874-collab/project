"""
测试数据定义
"""
from datetime import datetime, timedelta


class CandlestickTestData:
    """Candlestick API 测试数据"""

    # 有效的交易对
    VALID_INSTRUMENTS = [
        "BTC_USDT",
        "ETH_USDT",
        "CRO_USDT",
        "DOGE_USDT",
        "SOL_USDT"
    ]

    # 有效的时间周期
    VALID_TIMEFRAMES = [
        "1m",  # 1 minute
        "5m",  # 5 minutes
        "15m",  # 15 minutes
        "30m",  # 30 minutes
        "1h",  # 1 hour
        "4h",  # 4 hours
        "6h",  # 6 hours
        "12h",  # 12 hours
        "1D",  # 1 day
        "7D",  # 7 days
        "14D",  # 14 days
        "1M"  # 1 month
    ]

    # 正向测试用例数据
    POSITIVE_TEST_CASES = [
        {
            "case_id": "TC_001",
            "description": "获取 BTC_USDT 1小时 K线数据（最近100条）",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 105
            },
            "expected": {
                "status_code": 200,
                "has_result": True,
                "min_data_points": 1
            }
        },
        {
            "case_id": "TC_002",
            "description": "获取 ETH_USDT 5分钟 K线数据（指定时间范围）",
            "params": {
                "instrument_name": "ETH_USDT",
                "timeframe": "5m",
                "start_ts": int((datetime.now() - timedelta(days=1)).timestamp() * 1000),
                "end_ts": int(datetime.now().timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "has_result": True,
                "min_data_points": 1
            }
        },
        {
            "case_id": "TC_003",
            "description": "获取 CRO_USDT 1天 K线数据（最近30条）",
            "params": {
                "instrument_name": "CRO_USDT",
                "timeframe": "1D",
                "count": 30
            },
            "expected": {
                "status_code": 200,
                "has_result": True,
                "min_data_points": 1
            }
        },
        {
            "case_id": "TC_004",
            "description": "获取最小数量 K线（count=1）",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 1
            },
            "expected": {
                "status_code": 200,
                "has_result": True,
                "exact_data_points": 1
            }
        },
        {
            "case_id": "TC_005",
            "description": "获取最大数量 K线（count=300）",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1m",
                "count": 300
            },
            "expected": {
                "status_code": 200,
                "has_result": True,
                "max_data_points": 300
            }
        }
    ]




    # 边界测试数据
    BOUNDARY_TEST_CASES = [
        {
            "case_id": "TC_BOUND_001",
            "description": "count = 0（边界值）",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 0
            },
            "expected": {
                "status_code": [400, 422]
            }
        },
        {
            "case_id": "TC_BOUND_002",
            "description": "极早的历史时间",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1D",
                "start_ts": 946684800000,  # 2000-01-01
                "end_ts": 978307200000  # 2001-01-01
            },
            "expected": {
                "status_code": 200,
                "may_be_empty": True
            }
        },
        {
            "case_id": "TC_BOUND_003",
            "description": "未来时间",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "start_ts": int((datetime.now() + timedelta(days=365)).timestamp() * 1000),
                "end_ts": int((datetime.now() + timedelta(days=366)).timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "should_be_empty": True
            }
        }
    ]

    # 性能测试数据
    PERFORMANCE_TEST_CASES = [
        {
            "case_id": "TC_PERF_001",
            "description": "大数据量请求（300条 1分钟数据）",
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1m",
                "count": 300
            },
            "performance_criteria": {
                "max_response_time_ms": 2000,
                "max_response_size_mb": 5
            }
        },
        {
            "case_id": "TC_PERF_002",
            "description": "并发请求测试",
            "concurrent_requests": 10,
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 100
            },
            "performance_criteria": {
                "max_avg_response_time_ms": 3000,
                "success_rate_percent": 95
            }
        }
    ]

 # 提供便捷方法获取测试用例
# @classmethod    def get_case(cls, case_id: str, case_type: str = "positive"):        """        根据 case_id 获取测试用例                Args:            case_id: 测试用例ID，如 "TC_POS_001"            case_type: 用例类型 - "positive", "negative", "boundary"                Returns:            dict: 测试用例数据                Raises:            KeyError: 如果 case_id 不存在        """        case_map = {            "positive": cls.POSITIVE_CASES,            "negative": cls.NEGATIVE_CASES,            "boundary": cls.BOUNDARY_CASES        }                cases = case_map.get(case_type.lower())        if not cases:            raise ValueError(f"Invalid case_type: {case_type}")                if case_id not in cases:            raise KeyError(f"Case ID '{case_id}' not found in {case_type} cases")                return cases[case_id]        @classmethod    def get_all_cases(cls, case_type: str = "positive"):        """        获取某类型的所有测试用例                Args:            case_type: 用例类型                Returns:            list: 测试用例列表        """        case_map = {            "positive": cls.POSITIVE_CASES,            "negative": cls.NEGATIVE_CASES,            "boundary": cls.BOUNDARY_CASES        }                cases = case_map.get(case_type.lower())        if not cases:            raise ValueError(f"Invalid case_type: {case_type}")                return list(cases.values())        @classmethod    def get_case_ids(cls, case_type: str = "positive"):        """        获取某类型的所有测试用例ID                Args:            case_type: 用例类型                Returns:            list: 测试用例ID列表        """        case_map = {            "positive": cls.POSITIVE_CASES,            "negative": cls.NEGATIVE_CASES,            "boundary": cls.BOUNDARY_CASES        }                cases = case_map.get(case_type.lower())        if not cases:            raise ValueError(f"Invalid case_type: {case_type}")                return list(cases.keys())

class ExpectedDataStructure:
    """期望的响应数据结构"""

    RESPONSE_SCHEMA = {
        "code": int,
        "method": str,
        "result": {
            "instrument_name": str,
            "interval": str,
            "data": [
                {
                    "t": int,  # timestamp
                    "o": float,  # open
                    "h": float,  # high
                    "l": float,  # low
                    "c": float,  # close
                    "v": float  # volume
                }
            ]
        }
    }

    CANDLESTICK_FIELDS = ["t", "o", "h", "l", "c", "v"]

    REQUIRED_FIELDS = {
        "response": ["code", "method", "result"],
        "result": ["instrument_name", "interval", "data"],
        "candlestick": CANDLESTICK_FIELDS
    }