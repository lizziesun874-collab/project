"""
config/test_data/orderbook_cases.py
订单簿测试用例数据
"""
class OrderbookCases:
    # 订单簿测试用例
    CASES = {
        "TC_BOOK_001": {
            "case_id": "TC_BOOK_001",
            "description": "订阅订单簿数据 - BTC_USDT - 深度 10",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "BTCUSD-PERP",
                "depth": 10
            },
            "expected": {
                "subscription_success": True,
                "message_count": 1,
                "required_fields": ["instrument_name", "subscription", "channel", "data"],
                "data_fields": ["bids", "asks", "t"],
                "min_bids": 1,
                "min_asks": 1
            }
        },

        "TC_BOOK_002": {
            "case_id": "TC_BOOK_002",
            "description": "订阅订单簿数据 - ETH_USDT - 深度 50",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "ETHUSD-PERP",
                "depth": 50
            },
            "expected": {
                "subscription_success": True,
                "message_count": 1,
                "required_fields": ["instrument_name", "subscription", "channel", "data"],
                "data_fields": ["bids", "asks", "t"],
                "min_bids": 1,
                "min_asks": 1
            }
        },

        "TC_BOOK_003": {
            "case_id": "TC_BOOK_003",
            "description": "订阅订单簿数据 - 无效交易对",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "INVALID_PAIR",
                "depth": 10
            },
            "expected": {
                "subscription_success": False,
                "error_code": 10004
            }
        },

        "TC_BOOK_004": {
            "case_id": "TC_BOOK_004",
            "description": "订阅订单簿数据 - BTC_USDT - 深度 150",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "BTC_USDT",
                "depth": 150
            },
            "expected": {
                "subscription_success": True,
                "message_count": 1,
                "required_fields": ["instrument_name", "subscription", "channel", "data"],
                "data_fields": ["bids", "asks", "t"],
                "min_bids": 1,
                "min_asks": 1
            }
        },

        "TC_BOOK_005": {
            "case_id": "TC_BOOK_005",
            "description": "订阅多个订单簿频道",
            "channel_type": "orderbook",
            "params": {
                "channels": [
                    {"instrument_name": "BTC_USDT", "depth": 10},
                    {"instrument_name": "ETH_USDT", "depth": 10}
                ]
            },
            "expected": {
                "subscription_success": True,
                "message_count": 2,
                "required_fields": ["instrument_name", "subscription", "channel", "data"]
            }
        },

        "TC_BOOK_006": {
            "case_id": "TC_BOOK_006",
            "description": "订阅后取消订阅",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "BTC_USDT",
                "depth": 10
            },
            "expected": {
                "subscription_success": True,
                "unsubscribe_success": True
            }
        },

        "TC_BOOK_007": {
            "case_id": "TC_BOOK_007",
            "description": "验证订单簿数据更新",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "BTC_USDT",
                "depth": 10
            },
            "expected": {
                "subscription_success": True,
                "message_count": 5,  # 接收 5 条更新消息
                "data_fields": ["bids", "asks", "t"]
            }
        },

        "TC_BOOK_008": {
            "case_id": "TC_BOOK_008",
            "description": "验证买卖盘价格排序",
            "channel_type": "orderbook",
            "params": {
                "instrument_name": "BTC_USDT",
                "depth": 10
            },
            "expected": {
                "subscription_success": True,
                "bids_sorted": "desc",  # 买盘从高到低
                "asks_sorted": "asc"  # 卖盘从低到高
            }
        }
    }



