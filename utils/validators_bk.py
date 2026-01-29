"""
数据验证器
"""
import logging
from typing import Dict, Any, List,Tuple
from hisdata.test_data import ExpectedDataStructure


class ResponseValidator:
    """响应数据验证器"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_response_structure(self, response: Dict[str, Any]) -> Tuple:
        """
        验证响应结构

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # 检查顶层字段
        for field in ExpectedDataStructure.REQUIRED_FIELDS["response"]:
            if field not in response:
                errors.append(f"Missing required field: {field}")

        # 检查 result 字段
        if "result" in response:
            result = response["result"]
            if isinstance(result, dict):
                for field in ExpectedDataStructure.REQUIRED_FIELDS["result"]:
                    if field not in result:
                        errors.append(f"Missing required field in result: {field}")

                # 检查 data 数组
                if "data" in result and isinstance(result["data"], list):
                    if len(result["data"]) > 0:
                        candlestick = result["data"][0]
                        for field in ExpectedDataStructure.CANDLESTICK_FIELDS:
                            if field not in candlestick:
                                errors.append(f"Missing candlestick field: {field}")

        is_valid = len(errors) == 0
        return is_valid, errors

    def validate_candlestick_data(self, data:List[Dict]) -> Tuple:

        errors = []

        if not data:
            return True, []

        for idx, candle in enumerate(data):
            # 验证 OHLC 关系
            #o, h, l, c = candle.get("o"), candle.get("h"), candle.get("l"), candle.get("c")
            o = float(candle.get("o")) if candle.get("o") is not None else None
            h = float(candle.get("h")) if candle.get("h") is not None else None
            l = float(candle.get("l")) if candle.get("l") is not None else None
            c = float(candle.get("c")) if candle.get("c") is not None else None
            v = float(candle.get("v")) if candle.get("v") is not None else None
            t = int(candle.get("t")) if candle.get("t") is not None else None


            if None in [o, h, l, c]:
                errors.append(f"Candle {idx}: Missing OHLC values")
                continue

            # High 应该是最高价
            if h < o or h < c or h < l:
                errors.append(f"Candle {idx}: High price invalid (h={h}, o={o}, l={l}, c={c})")

            # Low 应该是最低价
            if l > o or l > c or l > h:
                errors.append(f"Candle {idx}: Low price invalid (h={h}, o={o}, l={l}, c={c})")

            # 价格应该为正数
            if any(price <= 0 for price in [o, h, l, c]):
                errors.append(f"Candle {idx}: Negative or zero price detected")

            # 成交量应该为非负数
            if v is not None and v < 0:
                errors.append(f"Candle {idx}: Negative volume (v={v})")

            # 时间戳应该为正数
            if t is not None and t <= 0:
                errors.append(f"Candle {idx}: Invalid timestamp (t={t})")

        # 验证时间序列顺序
        timestamps = [candle.get("t") for candle in data if candle.get("t") is not None]
        if len(timestamps) > 1:
            for i in range(1, len(timestamps)):
                if timestamps[i] <= timestamps[i - 1]:
                    errors.append(f"Timestamps not in ascending order at index {i}")
                    break

        is_valid = len(errors) == 0
        return is_valid, errors


    def validate_data_count(self, data:List[Dict], expected_count: int = None,max_count: int = None, min_count: int = None) -> Tuple:

        actual_count = len(data)

        if expected_count is not None:
            if actual_count != expected_count:
                return False, f"Expected {expected_count} data points, got {actual_count}"

        if max_count is not None:
            if actual_count > max_count:
                return False, f"Data count {actual_count} exceeds max {max_count}"

        if min_count is not None:
            if actual_count < min_count:
                return False, f"Data count {actual_count} below min {min_count}"

        return True, None


    def validate_instrument_name(self, response: Dict[str, Any],
                                 expected_instrument: str) -> Tuple:
        """验证交易对名称"""
        actual_instrument = response.get("result", {}).get("instrument_name")

        if actual_instrument != expected_instrument:
            return False, f"Expected instrument {expected_instrument}, got {actual_instrument}"

        return True, None


    def validate_timeframe(self, response: Dict[str, Any],
                           expected_timeframe: str) -> Tuple:
        """验证时间周期"""
        actual_interval = response.get("result", {}).get("interval")

        if actual_interval != expected_timeframe:
            return False, f"Expected timeframe {expected_timeframe}, got {actual_interval}"

        return True, None