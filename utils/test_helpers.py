"""
utils/test_helpers.py
测试辅助方法 - 提供可复用的测试逻辑
"""
import allure
from typing import Dict, Any, List
from utils.validators import (
    ResponseValidator,
    CandlestickValidator,
    DataCompletenessValidator
)


class TestHelpers:
    """测试辅助类 - 提供通用测试方法"""

    # ==================== 1. 通用验证方法 ====================

    @staticmethod
    def common_validation(
            result: Dict[str, Any],
            expected_status_code: int = 200,
            expected_response_code: int = 0,
            logger=None
    ):
        """
        通用验证 - HTTP 状态码 + 响应码

        Args:
            result: API 响应结果
            expected_status_code: 期望的 HTTP 状态码
            expected_response_code: 期望的响应码
            logger: 日志记录器
        """
        with allure.step("执行通用验证（HTTP状态码 + 响应码）"):
            # 验证 HTTP 状态码
            ResponseValidator.validate_status_code(
                result,
                expected_status_code,
                logger
            )

            # 验证响应码
            ResponseValidator.validate_response_code(
                result["response"],
                expected_response_code,
                logger
            )


    # ==================== 2. K线数据综合验证 ====================

    @staticmethod
    def validate_candlestick_data(
            data:List[Dict[str, Any]],
    min_price: float = None,
    max_price: float = None,
    expected_interval: int = None,
    tolerance: int = None,
    max_count: int = None,
    exact_count: int = None,
    logger = None
    ):
        """
        K线数据综合验证 - 包含 CandlestickValidator 的所有验证

        Args:
            K线数据列表
            min_price: 最低价格
            max_price: 最高价格
            expected_interval: 期望的时间间隔（毫秒）
            tolerance: 时间间隔允许的误差（毫秒）
            max_count: 最大数据数量
            exact_count: 精确数据数量
            logger: 日志记录器
        """
        with allure.step("K线数据综合验证"):
            # 1. 验证 K线数据结构
            CandlestickValidator.validate_candlestick_structure(data, logger)

            # 2. 验证 K线价格逻辑
            CandlestickValidator.validate_price_logic(data, logger)

            # 3. 验证时间戳顺序
            CandlestickValidator.validate_timestamps_order(data, logger)

            # 4. 验证价格范围（如果提供）
            if min_price is not None or max_price is not None:
                CandlestickValidator.validate_price_range(
                    data,
                    min_price=min_price,
                    max_price=max_price,
                    logger=logger
                )

            # 5. 验证时间间隔（如果提供）
            if expected_interval is not None:
                CandlestickValidator.validate_time_interval(
                    data,
                    expected_interval=expected_interval,
                    tolerance=tolerance,
                    logger=logger
                )

            # 6. 验证数据数量（如果提供）
            if max_count is not None or exact_count is not None:
                CandlestickValidator.validate_data_count(
                    data,
                    max_count=max_count,
                    exact_count=exact_count,
                    logger=logger
                )

            if logger:
                logger.info("✓ K线数据综合验证全部通过")


# ==================== 3. 数据完整性综合验证 ====================

    @staticmethod
    def validate_data_completeness(
            data:List[Dict[str, Any]],
    required_fields: List[tuple] = None,
    check_null_values: bool = True,
    check_duplicate_timestamps: bool = True,
    check_consistency: bool = True,
    logger = None
    ):
        """
        数据完整性综合验证 - 包含 DataCompletenessValidator 的所有验证

        Args:
            K线数据列表
            required_fields: 必需字段列表 [("short_name", "full_name"), ...]
            check_null_values: 是否检查空值
            check_duplicate_timestamps: 是否检查重复时间戳
            check_consistency: 是否检查数据一致性
            logger: 日志记录器
        """
        with allure.step("数据完整性综合验证"):
            # 1. 验证无缺失字段（如果提供）
            if required_fields is not None:
                DataCompletenessValidator.validate_no_missing_fields(
                    data,
                    required_fields,
                    logger
                )

            # 2. 验证无空值
            if check_null_values:
                DataCompletenessValidator.validate_no_null_values(
                    data,
                    fields_to_check=None,
                    logger=logger
                )

            # 3. 验证无重复时间戳
            if check_duplicate_timestamps:
                DataCompletenessValidator.validate_no_duplicate_timestamps(
                    data,
                    logger
                )

            # 4. 验证数据一致性
            if check_consistency:
                DataCompletenessValidator.validate_data_consistency(
                    data,
                    logger
                )

            if logger:
                logger.info("✓ 数据完整性综合验证全部通过")


# ==================== 4. 基础数据验证 ====================

    @staticmethod
    def basic_data_validation(result: Dict[str, Any], logger=None) -> List[Dict[str, Any]]:
        """
        基础数据验证 - 验证数据存在且不为空

        Args:
            result: API 响应结果
            logger: 日志记录器

        Returns:
            list: 返回数据列表
        """
        with allure.step("验证数据存在"):
            response = result["response"]
            data = ResponseValidator.validate_data_exists(response, logger)
            return data


# ==================== 5. 日志辅助方法 ====================

    @staticmethod
    def log_test_info(
            case_id: str,
            description: str,
            params: dict,
            priority: str = None,
            tags: list = None,
            logger=None
    ):
        """
        记录测试信息

        Args:
            case_id: 用例ID
            description: 用例描述
            params: 请求参数
            priority: 优先级
            tags: 标签列表
            logger: 日志记录器
        """
        if logger:
            logger.info(f"{'=' * 60}")
            logger.info(f"[{case_id}] Testing: {description}")

            if priority:
                logger.info(f"Priority: {priority}")

            if tags:
                logger.info(f"Tags: {', '.join(tags)}")

            logger.info(f"Request params: {params}")


    @staticmethod
    def log_test_result(case_id: str, result: Dict[str, Any], logger=None):
        """
        记录测试结果

        Args:
            case_id: 用例ID
            result: API 响应结果
            logger: 日志记录器
        """
        if logger:
            logger.info(f"Response status: {result['status_code']}")
            logger.info(f"Response code: {result['response'].get('code')}")


    @staticmethod
    def log_test_success(case_id: str, logger=None):
        """
        记录测试成功

        Args:
            case_id: 用例ID
            logger: 日志记录器
        """
        if logger:
            logger.info(f"✅ [{case_id}] All validations passed")
            logger.info(f"{'=' * 60}\n")


# ==================== 6. 完整测试流程（组合方法）====================

    @staticmethod
    def execute_basic_test(
            api_client,
            test_data: Dict[str, Any],
            save_response_func,
            logger=None,
            checkdata = True
    ) -> Dict[str, Any]:
        """
        执行基础测试流程 - 通用验证 + 数据存在验证

        Args:
            api_client: API 客户端
            test_测试用例数据
            save_response_func: 保存响应的函数
            logger: 日志记录器

        Returns:
            dict: 包含 result 和 data 的字典
        """
        case_id = test_data["case_id"]
        description = test_data["description"]
        params = test_data["params"]
        expected = test_data["expected"]

        # 步骤1: 发送请求
        with allure.step(f"步骤1: 发送请求 - {description}"):
            TestHelpers.log_test_info(
                case_id,
                description,
                params,
                priority=test_data.get("priority"),
                tags=test_data.get("tags"),
                logger=logger
            )

            result = api_client.get_candlestick(params)

            TestHelpers.log_test_result(case_id, result, logger)

        # 保存响应
        save_response_func(result, case_id.lower())

        # 步骤2: 通用验证
        with allure.step("步骤2: 执行通用验证"):
            TestHelpers.common_validation(
                result,
                expected_status_code=expected.get("status_code", 200),
                expected_response_code=expected.get("code", 0),
                logger=logger
            )

        # 步骤3: 验证数据存在
        if(checkdata):
            with allure.step("步骤3: 验证数据存在"):
                data = TestHelpers.basic_data_validation(result, logger)

            return {
                "result": result,
                "data": data
            }


    @staticmethod
    def execute_full_validation_test(
            api_client,
            test_data:Dict[str, Any],
    save_response_func,
    candlestick_params: Dict[str, Any] = None,
    completeness_params: Dict[str, Any] = None,
    logger = None
    ):
        """
        执行完整验证测试流程 - 通用验证 + K线验证 + 完整性验证

        Args:
            api_client: API 客户端
            test_测试用例数据
            save_response_func: 保存响应的函数
            candlestick_params: K线验证参数（传递给 validate_candlestick_data）
            completeness_params: 完整性验证参数（传递给 validate_data_completeness）
            logger: 日志记录器
        """
        # 执行基础测试
        test_result = TestHelpers.execute_basic_test(
            api_client,
            test_data,
            save_response_func,
            logger
        )

        data = test_result["data"]

        # 步骤4: K线数据验证
        if candlestick_params:
            with allure.step("步骤4: K线数据综合验证"):
                TestHelpers.validate_candlestick_data(
                    data=data,
                    **candlestick_params,
                    logger=logger
                )

        # 步骤5: 数据完整性验证
        if completeness_params:
            with allure.step("步骤5: 数据完整性综合验证"):
                TestHelpers.validate_data_completeness(
                    data=data,
                    **completeness_params,
                    logger=logger
                )

        # 记录测试成功
        TestHelpers.log_test_success(test_data["case_id"], logger)

    @staticmethod
    def validate_status_code_from_test_data(result: Dict[str, Any], test_data:Dict[str, Any], logger = None):

        expected_status_code = test_data.get("expected", {}).get("status_code")
        if expected_status_code is None:
        # 如果没有指定，默认期望 200
            expected_status_code = 200
            if logger:
                logger.warning("⚠️  测试数据中未指定 status_code，默认期望 200")
        # 获取实际状态码
        actual_status_code = result["status_code"]
        # 验证状态码
        if isinstance(expected_status_code, list):
        # 列表验证：实际状态码应该在列表中
            with allure.step(f"验证状态码在 {expected_status_code} 中"):
                assert actual_status_code in expected_status_code, f"Expected status code in {expected_status_code}, but got {actual_status_code}"
                if logger:
                    logger.info(f"✓ 状态码验证通过: {actual_status_code} in {expected_status_code}")
                    # 附加到 Allure 报告
                allure.attach(f"期望状态码: {expected_status_code}\n实际状态码: {actual_status_code}\n验证结果: ✅ 通过",                    name="状态码验证",                    attachment_type=allure.attachment_type.TEXT                )
        else: # 单个值验证：实际状态码应该等于期望值
               with allure.step(f"验证状态码 = {expected_status_code}"):
                    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"
                    if logger:
                        logger.info(f"✓ 状态码验证通过: {actual_status_code} == {expected_status_code}")
                        # 附加到 Allure 报告
                        allure.attach(                    f"期望状态码: {expected_status_code}\n实际状态码: {actual_status_code}\n验证结果: ✅ 通过",                    name="状态码验证",                    attachment_type=allure.attachment_type.TEXT                )

# ==================== 7. 标准字段定义（常用常量）====================

    @staticmethod
    def get_standard_candlestick_fields() -> List[tuple]:
        """
        获取标准 K线字段列表

        Returns:
            list: 标准字段列表 [("short_name", "full_name"), ...]
        """
        return [
            ("t", "timestamp"),
            ("o", "open"),
            ("h", "high"),
            ("l", "low"),
            ("c", "close"),
            ("v", "volume")        ]