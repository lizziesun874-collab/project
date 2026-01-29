"""
tests/test_orderbook.py
订单簿 WebSocket 接口测试
"""

import pytest
import asyncio
import allure
from config.config import Config

from utils.ws_test_helpers import  WebSocketTestHelper


@allure.epic("Crypto API WebSocket 测试")
@allure.feature("订单簿数据测试")
class TestOrderbook:
    """订单簿 WebSocket 接口测试类"""

    # ==================== 基础功能测试 ====================

    @allure.story("订阅订单簿 - BTC_USDT - 深度 10")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.parametrize("orderbook_case", ["TC_BOOK_001"], indirect=True)
    async def test_book_001_subscribe_btc_depth_10(
            self,
            ws_client,
            test_logger,
            save_response,
            orderbook_case,
            validator):
        """TC_BOOK_001: 订阅订单簿数据 - BTC_USDT - 深度 10"""

        case = orderbook_case

        with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
            test_logger.info(f"测试用例: {case['case_id']}")
            test_logger.info(f"描述: {case['description']}")
            test_logger.info(f"请求参数: {case['params']}")
        # 调试信息
        test_logger.info(f"WebSocket URL: {ws_client.ws_url}")
        test_logger.info(f"超时时间: {ws_client.timeout}秒")
        test_logger.info(f"连接状态: {await ws_client.is_connected()}")

        # assert ws_client.ws is not None, "WebSocket 对象不应为 None"
        # assert not ws_client.ws.closed, "WebSocket 不应处于关闭状态"

        await WebSocketTestHelper.execute_subscribe_test(
            ws_client, test_logger, save_response, case, validator
        )

    # @allure.story("订阅订单簿 - ETH_USDT - 深度 50")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_002_subscribe_eth_depth_50(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_002: 订阅订单簿数据 - ETH_USDT - 深度 50"""
    #
    #     case = orderbook_case("TC_BOOK_002")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_subscribe_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )
    #
    # @allure.story("订阅订单簿 - 无效交易对")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_003_subscribe_invalid_pair(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_003: 订阅订单簿数据 - 无效交易对"""
    #
    #     case = orderbook_case("TC_BOOK_003")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_error_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )
    #
    # @allure.story("订阅订单簿 - 深度 150")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_004_subscribe_depth_150(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_004: 订阅订单簿数据 - BTC_USDT - 深度 150"""
    #
    #     case = orderbook_case("TC_BOOK_004")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_subscribe_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )
    #
    # # ==================== 高级功能测试 ====================
    #
    # @allure.story("订阅多个订单簿频道")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_005_subscribe_multiple_channels(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_005: 订阅多个订单簿频道"""
    #
    #     case = orderbook_case("TC_BOOK_005")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_multiple_subscribe_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )
    #
    # @allure.story("订阅后取消订阅")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_006_unsubscribe(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_006: 订阅后取消订阅"""
    #
    #     case = orderbook_case("TC_BOOK_006")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_unsubscribe_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )
    #
    # @allure.story("验证订单簿数据更新")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_007_data_updates(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_007: 验证订单簿数据更新"""
    #
    #     case = orderbook_case("TC_BOOK_007")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_data_update_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )
    #
    # @allure.story("验证买卖盘价格排序")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.asyncio
    # async def test_book_008_price_sorting(
    #         self,
    #         ws_client,
    #         test_logger,
    #         save_response,
    #         orderbook_case,
    #         validator):
    #     """TC_BOOK_008: 验证买卖盘价格排序"""
    #
    #     case = orderbook_case("TC_BOOK_008")
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         test_logger.info(f"测试用例: {case['case_id']}")
    #         test_logger.info(f"描述: {case['description']}")
    #         test_logger.info(f"请求参数: {case['params']}")
    #
    #     await self._execute_price_sorting_test(
    #         ws_client, test_logger, save_response, case, validator
    #     )

