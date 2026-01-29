"""
tests/test_candlestick_positive.py
正向测试用例 - 简化版通用验证
"""
import pytest
import allure
from typing import Dict, Any
from data import TestDataLoader
from utils.validators import ResponseValidator

# ✅ 将常量定义在类外部
CUSTOM_VALIDATION_CASES = [
    "TC_POS_001"
]


@allure.feature("K线数据接口")
@allure.story("正向测试")
class TestCandlestickPositive:
    """K线数据接口正向测试"""

    # ==================== 通用验证方法（仅验证状态码和响应码）====================

    def _common_validation(
            self,
            result: Dict[str, Any],
            test_data:Dict[str, Any],
            test_logger):

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

        with allure.step(f"步骤1: 发送请求 - {description}"):
            test_logger.info(f"{'=' * 60}")
            test_logger.info(f"[{case_id}] Testing: {description}")
            test_logger.info(f"Priority: {priority}, Tags: {tags}")
            test_logger.info(f"Request params: {test_data['params']}")

            result = api_client.get_candlestick(test_data["params"])

            test_logger.info(f"Response status: {result['status_code']}")
            test_logger.info(f"Response code: {result['response'].get('code')}")

        save_response(result, case_id.lower())

        with allure.step("步骤2: 执行通用验证（HTTP状态码 + 响应码）"):
            self._common_validation(result, test_data, test_logger)

        test_logger.info(f"✅ [{case_id}] All validations passed")
        test_logger.info(f"{'=' * 60}\n")


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

        test_data = positive_case("TC_POS_001")

        with allure.step("步骤1: 发送请求"):
            test_logger.info(f"{'=' * 60}")
            test_logger.info(f"Testing: {test_data['description']}")
            test_logger.info(f"Request params: {test_data['params']}")

            result = api_client.get_candlestick(test_data["params"])

            test_logger.info(f"Response status: {result['status_code']}")

        save_response(result, "tc_pos_001_custom")

        with allure.step("步骤2: 执行通用验证（HTTP状态码 + 响应码）"):
            self._common_validation(result, test_data, test_logger)

        # ==================== 以下是自定义验证 ====================

        response = result["response"]

        with allure.step("步骤3: 验证数据存在"):
            data = ResponseValidator.validate_data_exists(response, test_logger)



        test_logger.info("✅ TC_POS_001 所有验证通过")
        test_logger.info(f"{'=' * 60}\n")


