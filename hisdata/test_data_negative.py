from datetime import datetime, timedelta

class NegativeTestData:
    # 负向测试用例数据
    NEGATIVE_TEST_CASES = [
            {
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
            {
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
            },
            {
                "case_id": "TC_NEG_003",
                "description": "无效的时间周期",
                "params": {
                    "instrument_name": "BTC_USDT",
                    "timeframe": "99h"
                },
                "expected": {
                    "status_code": [400, 422],
                    "has_error": True
                }
            },
            {
                "case_id": "TC_NEG_004",
                "description": "count 超出最大限制",
                "params": {
                    "instrument_name": "BTC_USDT",
                    "timeframe": "1h",
                    "count": 10000
                },
                "expected": {
                    "status_code": [400, 422],
                    "has_error": True
                }
            },
            {
                "case_id": "TC_NEG_005",
                "description": "count 为负数",
                "params": {
                    "instrument_name": "BTC_USDT",
                    "timeframe": "1h",
                    "count": -10
                },
                "expected": {
                    "status_code": [400, 422],
                    "has_error": True
                }
            },
            {
                "case_id": "TC_NEG_006",
                "description": "start_ts 大于 end_ts",
                "params": {
                    "instrument_name": "BTC_USDT",
                    "timeframe": "1h",
                    "start_ts": int(datetime.now().timestamp() * 1000),
                    "end_ts": int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
                },
                "expected": {
                    "status_code": [400, 422],
                    "has_error": True
                }
            },
            {
                "case_id": "TC_NEG_007",
                "description": "无效的时间戳格式",
                "params": {
                    "instrument_name": "BTC_USDT",
                    "timeframe": "1h",
                    "start_ts": "invalid_timestamp"
                },
                "expected": {
                    "status_code": [400, 422],
                    "has_error": True
                }
            }
        ]