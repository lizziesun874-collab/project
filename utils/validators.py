"""
utils/validators.py
通用验证器 - 提供可复用的验证方法
"""
from typing import Dict, Any, List,Tuple
import allure


class ResponseValidator:
    """响应验证器 - 通用响应验证方法"""

    @staticmethod
    def validate_status_code(result: Dict[str, Any], expected_code: int = 200, logger=None):
        """
        验证 HTTP 状态码

        Args:
            result: API 响应结果
            expected_code: 期望的状态码
            logger: 日志记录器
        """
        with allure.step(f"验证 HTTP 状态码 = {expected_code}"):
            actual_code = result["status_code"]
            if isinstance(expected_code, list):
                # ✅ 修复：列表验证
                with allure.step(f"验证状态码在 {expected_code} 中"):
                    assert actual_code in expected_code, f"Expected status code in {expected_code}, but got {actual_code}"
                    if logger:
                        logger.info(f"✓ 状态码验证通过: {actual_code} in {expected_code}")
            else:        # ✅ 单个值验证
                with allure.step(f"验证状态码 = {expected_code}"):
                    assert actual_code == expected_code, f"Expected status code {expected_code}, but got {actual_code}"
                    if logger:
                        logger.info(f"✓ 状态码验证通过: {actual_code} == {expected_code}")

            if logger:
                logger.info(f"✓ HTTP 状态码验证通过: {actual_code}")

    @staticmethod
    def validate_response_code(response: Dict[str, Any], expected_code: int = 0, logger=None):
        """
        验证响应码

        Args:
            response: API 响应体
            expected_code: 期望的响应码
            logger: 日志记录器
        """
        with allure.step(f"验证响应码 = {expected_code}"):
            actual_code = response.get("code")
            assert actual_code == expected_code, \
                f"Expected code {expected_code}, got {actual_code}"

            if logger:
                logger.info(f"✓ 响应码验证通过: {actual_code}")

    @staticmethod
    def validate_has_field(data:Dict[str, Any], field_name: str, logger = None):
        """
        验证字段存在

        Args:
            数据字典
            field_name: 字段名
            logger: 日志记录器
        """
        with allure.step(f"验证字段存在: {field_name}"):
            assert field_name in data, f"Field '{field_name}' not found in response"

            if logger:
                logger.info(f"✓ 字段 '{field_name}' 存在")


    @staticmethod
    def validate_field_type(data:Dict[str, Any], field_name: str, expected_type: type, logger = None):
        """
        验证字段类型

        Args:
            数据字典
            field_name: 字段名
            expected_type: 期望的类型
            logger: 日志记录器
        """
        with allure.step(f"验证字段 '{field_name}' 类型为 {expected_type.__name__}"):
            assert field_name in data, f"Field '{field_name}' not found"
            actual_type = type(data[field_name])
            assert isinstance(data[field_name], expected_type), \
                f"Field '{field_name}' expected type {expected_type.__name__}, got {actual_type.__name__}"

            if logger:
                logger.info(f"✓ 字段 '{field_name}' 类型验证通过: {expected_type.__name__}")


    @staticmethod
    def validate_field_value(data:Dict[str, Any], field_name: str, expected_value: Any, logger = None):
        """
        验证字段值

        Args:
            数据字典
            field_name: 字段名
            expected_value: 期望的值
            logger: 日志记录器
        """
        with allure.step(f"验证字段 '{field_name}' = {expected_value}"):
            assert field_name in data, f"Field '{field_name}' not found"
            actual_value = data[field_name]
            assert actual_value == expected_value, \
                f"Field '{field_name}' expected {expected_value}, got {actual_value}"

            if logger:
                logger.info(f"✓ 字段 '{field_name}' 值验证通过: {expected_value}")


    @staticmethod
    def validate_data_exists(response: Dict[str, Any], logger=None) -> List[Dict[str, Any]]:
        """
        验证数据存在且不为空

        Args:
            response: API 响应体
            logger: 日志记录器

        Returns:
            list: 返回数据列表
        """
        with allure.step("验证数据存在"):
            assert "result" in response, "Response should contain 'result' field"
            result_data = response.get("result", {})

            assert "data" in result_data, "Result should contain 'data' field"
            data = result_data["data"]

            assert isinstance(data, list), "Data should be a list"
            assert len(data) > 0, "Data should not be empty"

            if logger:
                logger.info(f"✓ 数据存在，共 {len(data)} 条记录")

            return data


    @staticmethod
    def validate_message(response: Dict[str, Any], expected_message: str = None, logger=None):
        """
        验证响应消息

        Args:
            response: API 响应体
            expected_message: 期望的消息
            logger: 日志记录器
        """
        if expected_message:
            with allure.step(f"验证响应消息: {expected_message}"):
                actual_message = response.get("message", "")
                assert expected_message in actual_message, \
                    f"Expected message to contain '{expected_message}', got '{actual_message}'"

                if logger:
                    logger.info(f"✓ 响应消息验证通过: {actual_message}")


class CandlestickValidator:
    """K线数据验证器 - 专门用于 K线数据的验证"""

    @staticmethod
    def validate_candlestick_structure(data:List[Dict[str, Any]], logger = None):
        """
        验证 K线数据结构

        Args:
            K线数据列表
            logger: 日志记录器
        """
        with allure.step("验证 K线数据结构"):
            required_fields = [
                ("t", "timestamp"),
                ("o", "open"),
                ("h", "high"),
                ("l", "low"),
                ("c", "close"),
                ("v", "volume")
            ]

            # 验证前3条数据的结构
            sample_size = min(3, len(data))
            for i, candle in enumerate(data[:sample_size]):
                for field1, field2 in required_fields:
                    assert field1 in candle or field2 in candle, \
                        f"Candle {i} should have '{field1}' or '{field2}' field"

            if logger:
                logger.info(f"✓ K线数据结构验证通过（验证了前 {sample_size} 条数据）")


    @staticmethod
    def validate_price_logic(data:List[Dict[str, Any]], logger = None):
        """
        验证 K线价格逻辑

        Args:
            K线数据列表
            logger: 日志记录器
        """
        with allure.step("验证 K线价格逻辑"):
            for i, candle in enumerate(data):
                # 获取价格数据（支持两种字段名格式）
                open_price = float(candle.get("o") or candle.get("open"))
                high_price = float(candle.get("h") or candle.get("high"))
                low_price = float(candle.get("l") or candle.get("low"))
                close_price = float(candle.get("c") or candle.get("close"))
                volume = float(candle.get("v") or candle.get("volume"))

                # 验证价格关系：high >= open, close, low
                assert high_price >= open_price, \
                    f"Candle {i}: high ({high_price}) should >= open ({open_price})"
                assert high_price >= close_price, \
                    f"Candle {i}: high ({high_price}) should >= close ({close_price})"
                assert high_price >= low_price, \
                    f"Candle {i}: high ({high_price}) should >= low ({low_price})"

                # 验证价格关系：low <= open, close
                assert low_price <= open_price, \
                    f"Candle {i}: low ({low_price}) should <= open ({open_price})"
                assert low_price <= close_price, \
                    f"Candle {i}: low ({low_price}) should <= close ({close_price})"

                # 验证价格和成交量为正数
                assert open_price > 0, f"Candle {i}: open price should > 0"
                assert high_price > 0, f"Candle {i}: high price should > 0"
                assert low_price > 0, f"Candle {i}: low price should > 0"
                assert close_price > 0, f"Candle {i}: close price should > 0"
                assert volume >= 0, f"Candle {i}: volume should >= 0"

            if logger:
                logger.info(f"✓ K线价格逻辑验证通过（验证了 {len(data)} 条数据）")


    @staticmethod
    def validate_timestamps_order(data:List[Dict[str, Any]], logger = None):
        """
        验证时间戳顺序

        Args:
            K线数据列表
            logger: 日志记录器
        """
        with allure.step("验证时间戳顺序"):
            if len(data) < 2:
                if logger:
                    logger.warning("⚠️  数据量不足，跳过时间戳顺序验证")
                return

            timestamps = [int(candle.get("t") or candle.get("timestamp")) for candle in data]

            # 检查是升序还是降序
            is_ascending = all(
                timestamps[i] <= timestamps[i + 1]
                for i in range(len(timestamps) - 1)
            )
            is_descending = all(
                timestamps[i] >= timestamps[i + 1]
                for i in range(len(timestamps) - 1)
            )

            assert is_ascending or is_descending, \
                "Timestamps should be in order (ascending or descending)"

            order = "升序" if is_ascending else "降序"
            if logger:
                logger.info(f"✓ 时间戳顺序验证通过（{order}）")


    @staticmethod
    def validate_data_count(data:List[Dict[str, Any]], max_count: int = None, exact_count: int = None, logger = None):
        """
        验证数据数量

        Args:
            K线数据列表
            max_count: 最大数量限制
            exact_count: 精确数量
            logger: 日志记录器
        """
        actual_count = len(data)

        if exact_count is not None:
            with allure.step(f"验证数据数量 = {exact_count}"):
                assert actual_count == exact_count, \
                    f"Data count should = {exact_count}, got {actual_count}"

                if logger:
                    logger.info(f"✓ 数据数量验证通过: {actual_count} = {exact_count}")

        elif max_count is not None:
            with allure.step(f"验证数据数量 <= {max_count}"):
                assert actual_count <= max_count, \
                    f"Data count should <= {max_count}, got {actual_count}"

                if logger:
                    logger.info(f"✓ 数据数量验证通过: {actual_count} <= {max_count}")


    @staticmethod
    def validate_price_range(data:List[Dict[str, Any]],min_price: float = None,max_price: float = None,logger = None):
        """
        验证价格范围

        Args:
            K线数据列表
            min_price: 最低价格
            max_price: 最高价格
            logger: 日志记录器
        """
        with allure.step(f"验证价格范围: {min_price} ~ {max_price}"):
            for i, candle in enumerate(data):
                close_price = float(candle.get("c") or candle.get("close"))

                if min_price is not None:
                    assert close_price >= min_price, \
                        f"Candle {i}: price {close_price} < min {min_price}"

                if max_price is not None:
                    assert close_price <= max_price, \
                        f"Candle {i}: price {close_price} > max {max_price}"

            if logger:
                logger.info(f"✓ 价格范围验证通过: {min_price} ~ {max_price}（验证了 {len(data)} 条数据）")


    @staticmethod
    def validate_time_interval(data:List[Dict[str, Any]],expected_interval: int,tolerance: int = None,logger = None):
        """
        验证时间间隔

        Args:
            K线数据列表
            expected_interval: 期望的时间间隔（毫秒）
            tolerance: 允许的误差（毫秒）
            logger: 日志记录器
        """
        if len(data) < 2:
            if logger:
                logger.warning("⚠️  数据量不足，跳过时间间隔验证")
            return

        with allure.step(f"验证时间间隔 = {expected_interval}ms"):
            timestamps = [int(candle.get("t") or candle.get("timestamp")) for candle in data]
            time_diffs = [abs(timestamps[i + 1] - timestamps[i]) for i in range(len(timestamps) - 1)]

            if tolerance is None:
                tolerance = expected_interval * 0.1  # 默认允许 10% 误差

            # 检查大部分时间间隔是否符合预期
            valid_intervals = sum(
                1 for diff in time_diffs
                if abs(diff - expected_interval) <= tolerance
            )

            consistency_rate = valid_intervals / len(time_diffs) * 100

            # 要求至少 80% 的时间间隔符合预期
            assert consistency_rate >= 80, f"Time interval consistency rate {consistency_rate:.1f}% < 80%"
            if logger:
                logger.info(f"✓ 时间间隔验证通过: {consistency_rate:.1f}% 符合预期间隔 {expected_interval}ms")


class DataCompletenessValidator:
    """数据完整性验证器 - 验证数据的完整性"""

    @staticmethod
    def validate_no_missing_fields(data:List[Dict[str, Any]],required_fields: List[Tuple[str, str]],
    logger = None
    ):
        """
        验证数据无缺失字段

        Args:
            K线数据列表
            required_fields: 必需字段列表 [("short_name", "full_name"), ...]
            logger: 日志记录器
        """
        with allure.step("验证数据完整性 - 无缺失字段"):
            missing_count = 0

            for i, candle in enumerate(data):
                for field1, field2 in required_fields:
                    if field1 not in candle and field2 not in candle:
                        missing_count += 1
                        if logger:
                            logger.warning(f"⚠️  Candle {i} 缺失字段: {field1}/{field2}")

            assert missing_count == 0, f"Found {missing_count} missing fields in data"

            if logger:
                logger.info(f"✓ 数据完整性验证通过：无缺失字段（验证了 {len(data)} 条数据）")


    @staticmethod
    def validate_no_null_values(
            data: List[Dict[str, Any]],
            fields_to_check: List[str] = None,
            logger=None
    ):
        """
        验证数据无空值

        Args:
            K线数据列表
            fields_to_check: 需要检查的字段列表（None 表示检查所有字段）
            logger: 日志记录器
        """
        with allure.step("验证数据完整性 - 无空值"):
            null_count = 0

            for i, candle in enumerate(data):
                fields = fields_to_check if fields_to_check else candle.keys()

                for field in fields:
                    if field in candle and candle[field] is None:
                        null_count += 1
                        if logger:
                            logger.warning(f"⚠️  Candle {i} 字段 '{field}' 为空值")

            assert null_count == 0, f"Found {null_count} null values in data"

            if logger:
                logger.info(f"✓ 数据完整性验证通过：无空值（验证了 {len(data)} 条数据）")


    @staticmethod
    def validate_no_duplicate_timestamps(data: List[Dict[str, Any]], logger=None):
        """
        验证数据无重复时间戳

        Args:
            K线数据列表
            logger: 日志记录器
        """
        with allure.step("验证数据完整性 - 无重复时间戳"):
            timestamps = [int(candle.get("t") or candle.get("timestamp")) for candle in data]
            unique_timestamps = set(timestamps)

            duplicate_count = len(timestamps) - len(unique_timestamps)

            assert duplicate_count == 0, f"Found {duplicate_count} duplicate timestamps"

            if logger:
                logger.info(f"✓ 数据完整性验证通过：无重复时间戳（验证了 {len(data)} 条数据）")


    @staticmethod
    def validate_data_consistency(data: List[Dict[str, Any]], logger=None):
        """
        验证数据一致性（综合验证）

        Args:
            data: K线数据列表
            logger: 日志记录器
        """
        with allure.step("验证数据一致性"):
            # 验证所有数据的字段数量一致
            field_counts = [len(candle.keys()) for candle in data]
            unique_field_counts = set(field_counts)

            assert len(unique_field_counts) == 1, \
                f"Inconsistent field counts: {unique_field_counts}"

            # 验证所有数据的字段名称一致
            field_sets = [set(candle.keys()) for candle in data]
            first_fields = field_sets[0]

            for i, fields in enumerate(field_sets[1:], start=1):
                assert fields == first_fields, \
                    f"Candle {i} has different fields: {fields.symmetric_difference(first_fields)}"

            if logger:
                logger.info(f"✓ 数据一致性验证通过：所有数据字段结构一致（验证了 {len(data)} 条数据）")


    @staticmethod
    def validate_continuous_data(data:List[Dict[str, Any]],
    expected_interval: int,
    tolerance: int = None,
    logger = None
    ):
        """
        验证数据连续性（无时间间隙）

        Args:
            K线数据列表
            expected_interval: 期望的时间间隔（毫秒）
            tolerance: 允许的误差（毫秒）
            logger: 日志记录器
        """
        if len(data) < 2:
            if logger:
                logger.warning("⚠️  数据量不足，跳过数据连续性验证")
            return

        with allure.step("验证数据连续性 - 无时间间隙"):
            timestamps = [int(candle.get("t") or candle.get("timestamp")) for candle in data]

            if tolerance is None:
                tolerance = int(expected_interval * 0.1)

            gaps = []
            for i in range(len(timestamps) - 1):
                time_diff = abs(timestamps[i + 1] - timestamps[i])
                if abs(time_diff - expected_interval) > tolerance:
                    gaps.append({
                        "index": i,
                        "expected": expected_interval,
                        "actual": time_diff,
                        "gap": time_diff - expected_interval
                    })

            if gaps and logger:
                logger.warning(f"⚠️  发现 {len(gaps)} 个时间间隙")
                for gap in gaps[:5]:  # 只显示前5个
                    logger.warning(f"   位置 {gap['index']}: 期望 {gap['expected']}ms, 实际 {gap['actual']}ms")

            # 允许少量间隙（不超过5%）
            gap_rate = len(gaps) / (len(timestamps) - 1) * 100
            assert gap_rate <= 5, f"Too many gaps: {gap_rate:.1f}% > 5%"

            if logger:
                logger.info(f"✓ 数据连续性验证通过：间隙率 {gap_rate:.1f}% <= 5%")


