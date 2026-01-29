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
        test_result =TestHelpers.execute_basic_test(api_client, test_data, save_response, test_logger)
        with allure.step("步骤4: 验证数据条数符合 count 参数"):  # 从请求参数中获取 count 值
            request_count = test_data["params"].get("count")
            if request_count:
                test_logger.info(f"请求参数 count = {request_count}")
                # 方式1：验证精确数量（如果 API 保证返回精确数量）
                CandlestickValidator.validate_data_count(data=test_result['data'], exact_count=request_count,logger=test_logger )
            else:
                test_logger.warning("⚠️  请求参数中未指定 count，跳过数据条数验证")






