"""
tests/test_candlestick_positive.py
正向测试用例 - 简化版（使用综合验证方法）
"""
import pytest
import allure
from typing import Dict, Any
from data import TestDataLoader
from utils.validators import ResponseValidator, CandlestickValidator, DataCompletenessValidator
from utils.test_helpers import TestHelpers


# ✅ 将常量定义在类外部
CUSTOM_VALIDATION_CASES = [
    "TC_POS_001",# BTC 1小时 K线 - 有自定义验证
    "TC_POS_003"
]


@allure.feature("K线数据接口")
@allure.story("正向测试")
class TestCandlestickPositive:
    """K线数据接口正向测试"""

    # ==================== 通用验证方法（仅验证状态码和响应码和结果有data）====================

    def _common_validation(
            self,
            result: Dict[str, Any],
            test_data:Dict[str, Any],
            test_logger
    ):
        """
        通用验证逻辑 - 只验证 HTTP 状态码和响应码

        Args:
            result: API 响应结果
            test_测试用例数据
            test_logger: 日志记录器
        """
        expected = test_data["expected"]
        response = result["response"]

        # ✅ 1. 验证 HTTP 状态码
        ResponseValidator.validate_status_code(
            result,
            expected["status_code"],
            test_logger
        )

        # ✅ 2. 验证响应码
        ResponseValidator.validate_response_code(
            response,
            expected.get("code", 0),
            test_logger
        )
        # 3.验证数据是否存在data
        ResponseValidator.validate_data_exists(response, test_logger)

    # ==================== 综合验证方法1：K线数据验证 ====================

    def _validate_candlestick_data(
            self,
            data:list,
            min_price: float = None,
            max_price: float = None,
            expected_interval: int = None,
            tolerance: int = None,
            max_count: int = None,
            exact_count: int = None,
            test_logger=None
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
            test_logger: 日志记录器
        """
        with allure.step("K线数据综合验证"):
            # 1. 验证 K线数据结构
            CandlestickValidator.validate_candlestick_structure(data, test_logger)

            # 2. 验证 K线价格逻辑
            CandlestickValidator.validate_price_logic(data, test_logger)

            # 3. 验证时间戳顺序
            CandlestickValidator.validate_timestamps_order(data, test_logger)

            # 4. 验证价格范围（如果提供）
            if min_price is not None or max_price is not None:
                CandlestickValidator.validate_price_range(
                    data,
                    min_price=min_price,
                    max_price=max_price,
                    logger=test_logger
                )

            # 5. 验证时间间隔（如果提供）
            if expected_interval is not None:
                CandlestickValidator.validate_time_interval(
                    data,
                    expected_interval=expected_interval,
                    tolerance=tolerance,
                    logger=test_logger
                )

            # 6. 验证数据数量（如果提供）
            if max_count is not None or exact_count is not None:
                CandlestickValidator.validate_data_count(
                    data,
                    max_count=max_count,
                    exact_count=exact_count,
                    logger=test_logger
                )

            if test_logger:
                test_logger.info("✓ K线数据综合验证全部通过")

    # ==================== 综合验证方法2：数据完整性验证 ====================

    def _validate_data_completeness(
            self,
            data:list,
            required_fields: list = None,
            check_null_values: bool = True,
            check_duplicate_timestamps: bool = True,
            check_consistency: bool = True,
            test_logger=None
    ):
        """
        数据完整性综合验证 - 包含 DataCompletenessValidator 的所有验证

        Args:
            K线数据列表
            required_fields: 必需字段列表 [("short_name", "full_name"), ...]
            check_null_values: 是否检查空值
            check_duplicate_timestamps: 是否检查重复时间戳
            check_consistency: 是否检查数据一致性
            test_logger: 日志记录器
        """
        with allure.step("数据完整性综合验证"):
            # 1. 验证无缺失字段（如果提供）
            if required_fields is not None:
                DataCompletenessValidator.validate_no_missing_fields(
                    data,
                    required_fields,
                    test_logger
                )

            # 2. 验证无空值
            if check_null_values:
                DataCompletenessValidator.validate_no_null_values(
                    data,
                    fields_to_check=None,
                    logger=test_logger
                )

            # 3. 验证无重复时间戳
            if check_duplicate_timestamps:
                DataCompletenessValidator.validate_no_duplicate_timestamps(
                    data,
                    test_logger
                )

            # 4. 验证数据一致性
            if check_consistency:
                DataCompletenessValidator.validate_data_consistency(
                    data,
                    test_logger
                )

            if test_logger:
                test_logger.info("✓ 数据完整性综合验证全部通过")

    # ==================== 条件1：通用参数化测试 ====================

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "test_data",
        [
            case for case in TestDataLoader.get_all_cases("positive")
            if case["case_id"] not in CUSTOM_VALIDATION_CASES
        ],
        ids=lambda case: case["case_id"]
    )
    @allure.title("正向测试: {test_data[case_id]} - {test_data[description]}")
    def test_all_positive_cases(
            self,
            api_client,
            test_logger,
            save_response,
            test_data
    ):
        """
        ✅ 条件1：通用参数化测试

        功能：
        1. 自动运行 positive_cases.py 中的所有测试用例
        2. 排除 CUSTOM_VALIDATION_CASES 中定义的用例（避免重复执行）
        3. 只验证 HTTP 状态码和响应码
        """
        case_id = test_data["case_id"]
        description = test_data["description"]
        priority = test_data.get("priority", "N/A")
        tags = ", ".join(test_data.get("tags", []))

        allure.dynamic.description(f"""
        **测试用例ID**: {case_id}
        **测试描述**: {description}
        **优先级**: {priority}
        **标签**: {tags}
        **请求参数**: 
        ```json
        {test_data['params']}
        ```
        """)


        # ★ 使用 TestHelpers 执行基础测试
        TestHelpers.execute_basic_test(api_client, test_data, save_response, test_logger)
        #TestHelpers.basic_data_validation(save_response,test_logger)
        # 记录测试成功        T
        TestHelpers.log_test_success(case_id, test_logger)

    # ==================== 条件2：手动添加特定用例的自定义验证 ====================

    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.title("TC_POS_001: 获取 BTC 1小时 K线 - 自定义验证")
    def test_btc_1h_custom_validation(
            self,
            api_client,
            test_logger,
            save_response,
            positive_case
    ):
        """
        ✅ TC_POS_001: BTC 1小时 K线 - 使用综合验证方法

        验证内容：
        1. 通用验证：HTTP 状态码 + 响应码
        2. K线数据综合验证（价格范围、时间间隔等）
        3. 数据完整性综合验证
        """
        test_data = positive_case("TC_POS_001")


        # 设置 Allure 描述
        allure.dynamic.description(f"""        
        **测试用例ID**: TC_POS_001        
        **测试描述**: {test_data['description']}        
        **交易对**: {test_data['params']['instrument_name']}       
        **时间周期**: {test_data['params']['timeframe']}                
        **验证策略**:        
        - 价格范围: 1000 ~ 200000 USDT        
        - 时间间隔: 3600000ms (1小时)        
        - 完整性检查: 字段完整、无空值、无重复时间戳""")
        # ★ 使用 TestHelpers 执行完整验证
        TestHelpers.execute_full_validation_test(api_client=api_client, test_data=test_data,
                                                 save_response_func=save_response,
                                                 candlestick_params={
                                                                        "min_price": 1000,  # BTC 最低价格
                                                                        "max_price": 200000, # BTC 最高价格
                                                                        "expected_interval": 3600000,  # 1小时 = 3600000 毫秒
                                                                        "tolerance": 60000,          # 允许 1 分钟误差
                                                                     },
                                                 completeness_params={ "required_fields": TestHelpers.get_standard_candlestick_fields(),
                                                                       "check_null_values": True,
                                                                       "check_duplicate_timestamps": True,
                                                                       "check_consistency": True,},
                                                 logger=test_logger)

    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.title("TC_POS_003: ETH-USDT Count验证 - 自定义验证")
    def test_count_custom_validation(
            self,
            api_client,
            test_logger,
            save_response,
            positive_case
    ):
        """
        ✅ TC_POS_003: ETH-USDT Count验证 - 自定义验证

        验证内容：
        1. 通用验证：HTTP 状态码 + 响应码
        2. 数据Count验证
        """
        test_data = positive_case("TC_POS_003")

        with allure.step("步骤1: 发送请求"):
            test_logger.info(f"{'=' * 60}")
            test_logger.info(f"[TC_POS_003] Testing: {test_data['description']}")
            test_logger.info(f"Request params: {test_data['params']}")

            result = api_client.get_candlestick(test_data["params"])

            test_logger.info(f"Response status: {result['status_code']}")
            test_logger.info(f"Response code: {result['response'].get('code')}")

        save_response(result, "tc_pos_003_custom")

        with allure.step("步骤2: 执行通用验证（HTTP状态码 + 响应码）"):
            self._common_validation(result, test_data, test_logger)

        response = result["response"]

        with allure.step("步骤3: 验证数据存在"):
            data = ResponseValidator.validate_data_exists(response, test_logger)

        with allure.step("步骤4: 验证数据条数符合 count 参数"):  # 从请求参数中获取 count 值
            request_count = test_data["params"].get("count")
            if request_count:
                test_logger.info(f"请求参数 count = {request_count}")
                # 方式1：验证精确数量（如果 API 保证返回精确数量）
                CandlestickValidator.validate_data_count(data=data, exact_count=request_count,logger=test_logger )
            else:
                test_logger.warning("⚠️  请求参数中未指定 count，跳过数据条数验证")


