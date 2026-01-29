"""
data/performance_cases.py
性能测试用例数据定义
"""


class PerformanceCases:
    """性能测试用例数据"""

    CASES = {
        "TC_PERF_001": {"case_id": "TC_PERF_001", "description": "响应时间测试（1小时周期，小数据量）", "priority": "P0",
                        "tags": ["performance", "response_time", "smoke"],
                        "params": {"instrument_name": "BTCUSD-PERP", "timeframe": "1m", "count": 200},
                        "expected": {"status_code": 200, "code": 0, "method": "public/get-candlestick",
                                     "min_data_points": 20, "max_response_time": 2000,  # 毫秒
                                     "avg_response_time": 1000,  # 毫秒
                                     "success_rate": 100.0,
                                     "error_rate": 0.0},
                        "performance_metrics": {"p50": 800, "p90": 1200, "p95": 1500, "p99": 1800}},

    }
