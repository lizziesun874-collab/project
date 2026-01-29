"""
tests/test_candlestick_combinations.py
组合覆盖测试 - 参数轮询组合
"""
import pytest
import allure
from data.combination_cases import get_combination_cases
from utils.test_helpers import TestHelpers


@allure.feature("K线数据接口")
@allure.story("组合覆盖测试")
class TestCandlestickCombinations:
    """组合覆盖测试 - 轮询组合策略"""

    @pytest.mark.combination
    @pytest.mark.parametrize(
        "test_data",
        get_combination_cases(),
        ids=lambda case: case["case_id"]
    )
    @allure.title("组合测试: {test_data[case_id]} - {test_data[description]}")
    def test_parameter_combinations(
            self,
            api_client,
            test_logger,
            save_response,
            test_data
    ):
        """
        参数组合覆盖测试

        策略：轮询组合（Round-Robin）
        - 确保每个 INSTRUMENT 都被测试
        - 确保每个 TIMEFRAME 都被测试
        - 最小化测试用例数量

        验证内容：
        1. HTTP 状态码 = 200
        2. 响应码 = 0
        3. 数据存在且不为空
        """
        case_id = test_data["case_id"]
        description = test_data["description"]
        params = test_data["params"]

        # 设置 Allure 描述
        allure.dynamic.description(f"""
        **测试用例ID**: {case_id}
        **测试描述**: {description}
        **交易对**: {params['instrument_name']}
        **时间周期**: {params['timeframe']}
        **数据数量**: {params['count']}
        """)

        with allure.step(f"步骤1: 发送请求 - {description}"):
            # 记录测试信息
            TestHelpers.log_test_info(case_id, description, params, test_logger)

            # 发送请求
            result = api_client.get_candlestick(params)

            # 记录响应信息
            TestHelpers.log_test_result(case_id, result, test_logger)

        # 保存响应
        save_response(result, case_id.lower())

        with allure.step("步骤2: 执行通用验证"):
            # 使用通用验证方法
            TestHelpers.common_validation(
                result,
                expected_status_code=test_data["expected"]["status_code"],
                expected_response_code=test_data["expected"]["code"],
                logger=test_logger
            )

        with allure.step("步骤3: 验证数据存在"):
            # 验证数据存在
            data = TestHelpers.basic_data_validation(result, test_logger)

            # 附加数据信息到报告
            allure.attach(
                f"返回数据条数: {len(data)}",
                name="数据统计",
                attachment_type=allure.attachment_type.TEXT
            )