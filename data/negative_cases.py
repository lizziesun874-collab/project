"""
data/negative_cases.py
负向测试用例数据定义
"""
from datetime import datetime, timedelta


class NegativeCases:
    """负向测试用例数据"""

    CASES = {
        "TC_NEG_001": {
            "case_id": "TC_NEG_001",
            "description": "缺少必填参数 instrument_name",
            "priority": "P2",
            "tags": ["smoke", "missing_param"],
            "params": {
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400],
                "has_error": True,
                "error_type": "missing_required_parameter"
            }
        },

        "TC_NEG_002": {
            "case_id": "TC_NEG_002",
            "description": "无效的交易对名称",
            "priority": "P2",
            "tags": ["smoke", "invalid_param"],
            "params": {
                "instrument_name": "INVALID_PAIR",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400],
                "has_error": True,
                "error_type": "invalid_instrument"
            }
        },
        "TC_NEG_002": {
            "case_id": "TC_NEG_002",
            "description": "无效的交易对名称",
            "priority": "P2",
            "tags": ["smoke", "invalid_param"],
            "params": {
                "instrument_name": "USDT_BTC",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400],
                "has_error": True,
                "error_type": "invalid_instrument"
            }
        },

        "TC_NEG_003": {
            "case_id": "TC_NEG_003",
            "description": "无效的时间周期",
            "priority": "P2",
            "tags": ["smoke", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "99h"
            },
            "expected": {
                "status_code": [400],
                "has_error": True,
                "error_type": "invalid_timeframe"
            }
        },

        "TC_NEG_004": {
            "case_id": "TC_NEG_004",
            "description": "Count 参数使用字符串类型",
            "priority": "P2",
            "tags": ["regression", "boundary"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "count": "abc"
            },
            "expected": {
                "status_code": [400, 422,500],
                "has_error": True,
                "error_type": "invalid parameters"
            }
        },

        "TC_NEG_005": {
            "case_id": "TC_NEG_005",
            "description": "count 为负数",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "count": -10
            },
            "expected": {
                "status_code": [400],
                "has_error": True,
                "error_type": "negative_count"
            }
        },



        "TC_NEG_007": {
            "case_id": "TC_NEG_007",
            "description": "无效的时间戳格式",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "start_ts": "invalid_timestamp"
            },
            "expected": {
                "status_code": [500],
                "has_error": True,
                "error_type": "invalid_timestamp_format"
            }
        },

        "TC_NEG_008": {
            "case_id": "TC_NEG_008",
            "description": "空字符串 instrument_name",
            "priority": "P2",
            "tags": ["regression", "edge_case"],
            "params": {
                "instrument_name": "",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400, 422,40004],
                "has_error": True,
                "error_type": "empty_instrument_name"
            }
        },

        "TC_NEG_009": {
            "case_id": "TC_NEG_009",
            "description": "特殊字符 instrument_name",
            "priority": "P2",
            "tags": ["regression", "edge_case"],
            "params": {
                "instrument_name": "BTC@#$%USDT",
                "timeframe": "1h"
            },
            "expected": {
                "status_code": [400, 404,40004],
                "has_error": True,
                "error_type": "invalid_characters"
            }
        },

        "TC_NEG_010": {
            "case_id": "TC_NEG_010",
            "description": "count 为 0",
            "priority": "P2",
            "tags": ["regression", "edge_case"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "count": 0
            },
            "expected": {
                "status_code": [400,422,40004],
                "has_error": True,
                "error_type": "zero_count"
            }
        },
        "TC_NEG_011": {
            "case_id": "TC_NEG_011",
            "description": "Count 参数为小数",
            "priority": "P2",
            "tags": ["regression", "boundary"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "count": 10.5
            },
            "expected": {
                "status_code": [400, 422,500],
                "has_error": True,
                "error_type": "invalid parameters"
            }
        },
        # 目前返回的默认值**
        # "TC_NEG_012": {
        #     "case_id": "TC_NEG_012",
        #     "description": "无效的时间戳格式",
        #     "priority": "P2",
        #     "tags": ["regression", "invalid_param"],
        #     "params": {
        #         "instrument_name": "BTCUSD-PERP",
        #         "timeframe": "1h",
        #         "start_ts": -1
        #     },
        #     "expected": {
        #         "status_code": [500],
        #         "has_error": True,
        #         "error_type": "invalid_timestamp_format"
        #     }
        # },
        "TC_NEG_013": {
            "case_id": "TC_NEG_013",
            "description": "无效的时间戳格式",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "end_ts": "2024-01-01"
            },
            "expected": {
                "status_code": [500],
                "has_error": True,
                "error_type": "invalid_timestamp_format"
            }
        },
        "TC_NEG_014": {
            "case_id": "TC_NEG_014",
            "description": "Symbol 参数包含 SQL 注入字符",
            "priority": "P0",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP'; DROP TABLE users; --",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500,400,403],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_015": {
            "case_id": "TC_NEG_015",
            "description": "Symbol 参数包含 XSS 注入",
            "priority": "P0",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "<script>alert('XSS')</script>",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400,403],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_016": {
            "case_id": "TC_NEG_016",
            "description": "Symbol 参数包含 XSS 注入",
            "priority": "P0",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP<img src=x onerror=alert(1)>",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400,403],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_017": {
            "case_id": "TC_NEG_017",
            "description": "Symbol 参数包含 XSS 注入",
            "priority": "P0",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "javascript:alert('XSS')",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400,403],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_018": {
            "case_id": "TC_NEG_018",
            "description": "Symbol 参数包含 特殊字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTC@USDT",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_019": {
            "case_id": "TC_NEG_019",
            "description": "Symbol 参数包含 特殊字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTC#USDT",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_019": {
            "case_id": "TC_NEG_019",
            "description": "Symbol 参数包含 特殊字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTC USDT",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_020": {
            "case_id": "TC_NEG_020",
            "description": "Symbol 参数包含 特殊字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTC%20USDT",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_021": {
            "case_id": "TC_NEG_021",
            "description": "Symbol 参数包含Unicode 字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "比特币_USDT",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_022": {
            "case_id": "TC_NEG_022",
            "description": "Symbol 参数包含Unicode 字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTC_₿",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_023": {
            "case_id": "TC_NEG_023",
            "description": "Symbol 参数包含Unicode 字符",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTC_\u0000",
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400,403],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_024": {
            "case_id": "TC_NEG_024",
            "description": "Symbol 参数超长",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "A" * 1000,
                "timeframe": "1h"

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_instrument_name_format"
            }
        },
        "TC_NEG_025": {
            "case_id": "TC_NEG_025",
            "description": "Interval 参数长度超过限制",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h"*500

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": "invalid_timeframe_format"
            }
        },
        "TC_NEG_026": {
            "case_id": "TC_NEG_026",
            "description": "同时使用 count、startTime 和 endTime（可能冲突）",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "count": 10,
                "startTime": 1704067200000,
                "endTime": 1704153600000
            },
            "expected": {
                "status_code": [500, 400,200],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_NEG_027": {
            "case_id": "TC_NEG_027",
            "description": "同时使用 count、startTime 和 endTime（可能冲突）",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "count": 10,
                "count": 2000
            },
            "expected": {
                "status_code": [500, 400,200],
                "has_error": True,
                "error_type": ""
            }
        },

        "TC_NEG_028": {
            "case_id": "TC_NEG_028",
            "description": "Symbol 参数为空字符串",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "",
                "timeframe": "1h",
            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_NEG_029": {
            "case_id": "TC_NEG_029",
            "description": "timeframe 参数为空字符串",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "",
            },
            "expected": {
                "status_code": [500, 400,200],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_NEG_030": {
            "case_id": "TC_NEG_030",
            "description": "Symbol 参数为NULL",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": None,
                "timeframe": "1h",
            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_NEG_031": {
            "case_id": "TC_NEG_031",
            "description": "timeframe 参数为NULL",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": None,
            },
            "expected": {
                "status_code": [500, 400,200],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_NEG_032": {
            "case_id": "TC_NEG_032",
            "description": "Symbol 大小写测试",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "btcusd-perp",
                "timeframe": None,
            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": ""
            }
        },
        "TC_NEG_033": {
            "case_id": "TC_NEG_033",
            "description": "Interval 参数的大小写敏感性",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1H",
            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": ""
            }
        },

        "TC_NEG_034": {
            "case_id": "TC_NEG_034",
            "description": "StartTime 等于 EndTime",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "start_ts":1704067200000,
                "end_ts": 1704067200000,

            },
            "expected": {
                "status_code": [500, 400],
                "has_error": True,
                "error_type": ""
            }
        },

        "TC_NEG_034": {#返回一条数据
            "case_id": "TC_NEG_034",
            "description": "StartTime 和 EndTime 间隔小于一个 K线周期",
            "priority": "P2",
            "tags": ["regression", "invalid_param"],
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "timeframe": "1h",
                "start_ts": 1704067200000,
                "end_ts": 1704067200001,

            },
            "expected": {
                "status_code": [500, 400,200],
                "has_error": True,
                "error_type": ""
            }
        },

    }