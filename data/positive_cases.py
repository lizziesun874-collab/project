"""
data/positive_cases.py
正向测试用例数据定义
"""
from datetime import datetime, timedelta


class PositiveCases:
    """正向测试用例数据"""

    CASES = {
        "TC_POS_001": {
            "case_id": "TC_POS_001",
            "description": "获取 BTC 1小时 K线数据",
            "priority": "P0",
            "tags": ["smoke", "basic"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "has_data": True
            }
        },

        "TC_POS_002": {
            "case_id": "TC_POS_002",
            "description": "获取 ETH 5分钟 K线（指定时间范围）",
            "priority": "P0",
            "tags": ["smoke", "time_range"],
            "params": {
                "instrument_name": "ETHUSD-PERP",
                "timeframe": "5m",
                "start_ts": int((datetime.now() - timedelta(hours=2)).timestamp() * 1000),
                "end_ts": int(datetime.now().timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "has_data": True
            }
        },

        "TC_POS_003": {
            "case_id": "TC_POS_003",
            "description": "获取指定数量的 K线（count=50）",
            "priority": "P0",
            "tags": ["smoke", "count"],
            "params": {
                "instrument_name": "ETHUSD-PERP",
                "timeframe": "1h",
                "count": 50
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True,
                "has_data": True,
                "max_data_points": 50
            }
        },
        "TC_POS_004": {
            "case_id": "TC_POS_004",
            "description": "获取历史 K线数据（指定过去时间）",
            "priority": "P1",
            "tags": ["regression", "historical"],
            "params": {
                "instrument_name": "CROUSD-PERP",
                "timeframe": "2h",
                "start_ts": int((datetime.now() - timedelta(days=7)).timestamp() * 1000),
                "end_ts": int((datetime.now() - timedelta(days=6)).timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },

        "TC_POS_005": {
            "case_id": "TC_POS_005",
            "description": "获取历史 K线数据（只有start_ts）",
            "priority": "P1",
            "tags": ["regression", "historical"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "4h",
                "start_ts": int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },

        "TC_POS_006": {
            "case_id": "TC_POS_006",
            "description": "获取历史 K线数据（只有end_ts）",
            "priority": "P1",
            "tags": ["regression", "historical"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1D",
                "end_ts": int((datetime.now() - timedelta(days=6)).timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        },
        "TC_POS_007": {
            "case_id": "TC_POS_007",
            "description": "获取历史 K线数据（有start_ts,end_ts但是间隔时间超过1天）",
            "priority": "P1",
            "tags": ["regression", "historical"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1m",
                "start_ts": int((datetime.now() - timedelta(days=7)).timestamp() * 1000),
                "end_ts": int((datetime.now() - timedelta(days=5)).timestamp() * 1000)
            },
            "expected": {
                "status_code": 200,
                "code": 0,
                "has_result": True
            }
        }




    }