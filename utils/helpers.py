"""
utils/helpers.py - 辅助函数
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List


def save_response_to_file(response_data:Dict[str, Any],
                        test_case_id: str, directory: str = "reports/responses") -> str:
    # 创建目录（如果不存在）
    os.makedirs(directory, exist_ok=True)

    # 生成文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_case_id}_{timestamp}.json"
    filepath = os.path.join(directory, filename)

    # 保存 JSON 文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, indent=2, ensure_ascii=False)

    print(f"Response saved to: {filepath}")
    return filepath


def calculate_response_size(response_data:Dict[str, Any]) -> int:
    json_str = json.dumps(response_data)
    return len(json_str.encode('utf-8'))


def format_timestamp(timestamp_ms: int) -> str:
    """
    格式化毫秒时间戳为可读字符串

    Args:
        timestamp_ms: 毫秒级时间戳

    Returns:
        str: 格式化的时间字符串 "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")


def calculate_statistics(data_list: List[float]) -> Dict[str, float]:
    """
    计算数值列表的统计信息

    Args:
        data_list: 数值列表

    Returns:
        dict: 包含 min, max, avg, count 的字典
    """
    if not data_list:
        return {}

    return {
        "min": min(data_list),
        "max": max(data_list),
        "avg": sum(data_list) / len(data_list),
        "count": len(data_list)
    }


def compare_candlesticks(candle1: Dict[str, Any], candle2: Dict[str, Any]) -> Dict[str, Any]:
    """    比较两个 K线数据        Args:        candle1: 第一个 K线数据        candle2: 第二个 K线数据            Returns:        dict: 差异字典    """


    differences = {}
    for key in ["o", "h", "l", "c", "v"]:        val1 = candle1.get(key)
    val2 = candle2.get(key)
    if val1 != val2:            differences[key] = {"candle1": val1, "candle2": val2,
                                                    "diff": abs(val1 - val2) if val1 and val2 else None}
    return differences
def validate_timestamp_range(start_ts: int, end_ts: int, max_days: int = 365) -> tuple:
    """    验证时间戳范围        Args:        start_ts: 开始时间戳（毫秒）        end_ts: 结束时间戳（毫秒）        max_days: 最大天数限制            Returns:        tuple: (is_valid, error_message)    """
    if start_ts >= end_ts:        return False, "start_ts must be less than end_ts"
    time_diff_ms = end_ts - start_ts
    time_diff_days = time_diff_ms / (1000 * 60 * 60 * 24)
    if time_diff_days > max_days:        return False, f"Time range exceeds {max_days} days"
    return True, None
def generate_test_report(test_results: List[Dict[
    str, Any]], output_file: str = "reports/summary.json") -> str:
    """    生成测试报告
    Args:        test_results: 测试结果列表
                output_file: 输出文件路径
                Returns:        str: 报告文件路径    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result.get("status") == "passed")
    failed_tests = total_tests - passed_tests
    summary = {"timestamp": datetime.now().isoformat(), "total_tests": total_tests, "passed": passed_tests,
               "failed": failed_tests,
               "pass_rate": f"{(passed_tests / total_tests * 100):.2f}%" if total_tests > 0 else "0%",
               "results": test_results}
    with open(output_file, 'w', encoding='utf-8') as f:        json.dump(summary, f, indent=2, ensure_ascii=False)
    return output_file
