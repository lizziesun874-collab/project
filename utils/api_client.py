"""
API 客户端封装
"""
import requests
import logging
import time
import json
from typing import Dict, Any, Optional
from config.config import Config


class APIClient:
    """API 客户端类"""

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.timeout = Config.TIMEOUT
        self.session = requests.Session()
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def get_candlestick(
            self,
            params: Dict[str, Any],
            headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        获取 K线数据

        Args:
            params: 请求参数
            headers: 请求头

        Returns:
            响应数据字典，包含 response、status_code、response_time 等
        """
        url = Config.get_full_url("candlestick")

        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "CryptoAPI-Test/1.0"
            }

        self.logger.info(f"Request URL: {url}")
        self.logger.info(f"Request Params: {json.dumps(params, indent=2)}")

        start_time = time.time()

        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            response_time = (time.time() - start_time) * 1000  # ms

            self.logger.info(f"Response Status: {response.status_code}")
            self.logger.info(f"Response Time: {response_time:.2f}ms")

            # 尝试解析 JSON
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                response_json = {"error": "Invalid JSON response"}

            return {
                "response": response_json,
                "status_code": response.status_code,
                "response_time": response_time,
                "headers": dict(response.headers),
                "url": response.url,
                "request_params": params
            }

        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout after {self.timeout}s")
            return {
                "error": "Timeout",
                "response_time": (time.time() - start_time) * 1000,
                "request_params": params
            }

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {
                "error": str(e),
                "response_time": (time.time() - start_time) * 1000,
                "request_params": params
            }

    def get_multiple_candlesticks(self, params_list: list) -> list:
        """
        批量获取 K线数据

        Args:
            params_list: 参数列表

        Returns:
            响应列表
        """
        results = []
        for params in params_list:
            result = self.get_candlestick(params)
            results.append(result)
            time.sleep(0.1)  # 避免请求过快

        return results

    def close(self):
        """关闭会话"""
        self.session.close()