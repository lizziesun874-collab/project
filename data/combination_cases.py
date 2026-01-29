"""
data/combination_cases.py
组合测试用例数据生成
"""

# 时间周期
TIMEFRAMES = [
    "5m",  # 5分钟
    "15m",  # 15分钟
    "30m",  # 30分钟
    "1h",  # 1小时
    "2h",  # 2小时
    "4h",  # 4小时
    "12h",  # 12小时
    "1D",  # 1天
    "7D",  # 1周
    "14D",  # 2周
    "1M",  # 1月
]

# 常用交易对
INSTRUMENTS = [
    "BTCUSD-PERP",
    "ETHUSD-PERP",
    "CROUSD-PERP",
]


def generate_round_robin_combinations(list1, list2):
    """
    轮询组合生成器 - 确保每个值都被覆盖

    Args:
        list1: 第一个参数列表
        list2: 第二个参数列表

    Returns:
        list: 组合列表 [(item1, item2), ...]
    """
    max_len = max(len(list1), len(list2))
    combinations = []

    for i in range(max_len):
        item1 = list1[i % len(list1)]
        item2 = list2[i % len(list2)]
        combinations.append((item1, item2))

    return combinations


def generate_combination_test_cases():
    """
    生成组合测试用例

    Returns:
        list: 测试用例列表
    """
    combinations = generate_round_robin_combinations(INSTRUMENTS, TIMEFRAMES)
    test_cases = []

    for i, (instrument, timeframe) in enumerate(combinations, 1):
        case = {
            "case_id": f"TC_COMBO_{i:03d}",
            "description": f"获取 {instrument} {timeframe} K线数据",
            "priority": "P2",
            "tags": ["combination", "coverage"],
            "params": {
                "instrument_name": instrument,
                "timeframe": timeframe,
                "count": 100
            },
            "expected": {
                "status_code": 200,
                "code": 0
            }
        }
        test_cases.append(case)

    return test_cases


# 生成测试用例
COMBINATION_CASES = generate_combination_test_cases()


# 提供获取用例的方法
def get_combination_cases():
    """获取所有组合测试用例"""
    return COMBINATION_CASES


def get_combination_case_by_id(case_id: str):
    """根据 case_id 获取单个用例"""
    for case in COMBINATION_CASES:
        if case["case_id"] == case_id:
            return case
    return None