"""
utils/validators.py
通用验证器 - 提供可复用的验证方法
"""
from typing import Dict, Any, List
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
            assert actual_code == expected_code, \
                f"Expected status code {expected_code}, got {actual_code}"

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

        with allure.step(f"验证字段存在: {field_name}"):
            assert field_name in data, f"Field '{field_name}' not found in response"

            if logger:
                logger.info(f"✓ 字段 '{field_name}' 存在")


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