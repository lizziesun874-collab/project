"""
data/boundary_cases.py
边界测试用例数据定义
"""
from datetime import datetime, timedelta


class BoundaryCases:
    """边界测试用例数据"""

    CASES = {
        "TC_BND_001": {
            "case_id": "TC_BND_001",
            "description": "测试最小 count=1",
            "priority": "P1",
            "tags": ["boundary", "min_value"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "count": 1
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "exact_count": 1
            }
        },

        "TC_BND_002": {
            "case_id": "TC_BND_002",
            "description": "测试最大 count=300",
            "priority": "P1",
            "tags": ["boundary", "max_value"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1m",
                "count": 300
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "max_data_points": 300
            }
        },

        "TC_BND_003": {
            "case_id": "TC_BND_003",
            "description": "测试默认 count（不传参数）",
            "priority": "P1",
            "tags": ["boundary", "default_value"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "default_count": 25
            }
        },

        "TC_BND_004": {
            "case_id": "TC_BND_004",
            "description": "测试最短时间范围（1分钟）",
            "priority": "P2",
            "tags": ["boundary", "time_range"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1m",
                "start_ts": int((datetime.now() - timedelta(minutes=1)).timestamp() * 1000),
                "end_ts": int(datetime.now().timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },


        "TC_BND_005": {
            "case_id": "TC_BND_005",
            "description": "测试最长时间范围（90天）",
            "priority": "P2",
            "tags": ["boundary", "time_range"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1D",
                "start_ts": int((datetime.now() - timedelta(days=90)).timestamp() * 1000),
                "end_ts": int(datetime.now().timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },

        "TC_BND_007": {#实际返回200
            "case_id": "TC_BND_007",
            "description": "start_ts 大于 end_ts",
            "priority": "P2",
            "tags": ["regression", "invalid_time_range"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "start_ts": int(datetime.now().timestamp() * 1000),
                "end_ts": int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
            },
            "expected": {
                "status_code": [200],
                "has_error": True,
                "error_type": "invalid_time_range"
            }
        },
        "TC_BND_008": {#Default is M1
            "case_id": "TC_BND_008",
            "description": "缺少必填参数 timeframe",
            "priority": "P0",
            "tags": ["smoke", "missing_param"],
            "params": {
                "instrument_name": "BTC_USDT"
            },
            "expected": {
                "status_code": [200],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_BND_009": {#200,但是无数据
            "case_id": "TC_BND_009",
            "description": "未来时间范围",
            "priority": "P2",
            "tags": ["regression", "edge_case"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1h",
                "start_ts": int((datetime.now() + timedelta(days=1)).timestamp() * 1000),
                "end_ts": int((datetime.now() + timedelta(days=2)).timestamp() * 1000)
            },
            "expected": {
                "status_code": [200],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_BND_010": {
            "case_id": "TC_BND_010",
            "description": "验证获取最早的历史数据",
            "priority": "P2",
            "tags": ["regression", "edge_case"],
            "params": {
                "instrument_name": "BTC_USDT",
                "timeframe": "1D",
                "start_ts": 1262304000000

            },
            "expected": {
                "status_code": [200],
                "has_error": True,
                "error_type": ""
            }
        },
    }