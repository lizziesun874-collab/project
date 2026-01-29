"""
tests/test_candlestick_negative.py
K线数据接口负向测试 - 测试异常输入和错误处理
"""
import pytest
import allure

from data import TestDataLoader
from hisdata.test_data_negative import NegativeTestData
from utils.test_helpers import TestHelpers


@allure.feature("K线数据接口")
@allure.story("负向测试 - 异常场景")
@allure.severity(allure.severity_level.CRITICAL)
class TestCandlestickNegative:
    """K线数据接口负向测试类"""

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "test_data",
        [
            case for case in TestDataLoader.get_all_cases("negative")

        ],
        ids=lambda case: case["case_id"]
    )
    @allure.title("负向测试: {test_data[case_id]} - {test_data[description]}")
    def test_all_negative_cases(
            self,
            api_client,
            test_logger,
            save_response,
            test_data
    ):
        """
        ✅ 条件1：通用参数化测试
        """
        case_id = test_data["case_id"]
        description = test_data["description"]
        params = test_data["params"]
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
        # 步骤1: 发送请求
        with allure.step(f"步骤1: 发送请求 - {description}"):
            TestHelpers.log_test_info(case_id, description, params, logger=test_logger)
            result = api_client.get_candlestick(params)
            TestHelpers.log_test_result(case_id, result, test_logger)
            # 保存响应
            save_response(result, case_id.lower())

        # ★ 使用 TestHelpers 执行基础测试
        TestHelpers.validate_status_code_from_test_data(result, test_data, test_logger)
        # TestHelpers.basic_data_validation(save_response,test_logger)
        # 记录测试成功        T
        TestHelpers.log_test_success(case_id, test_logger)

