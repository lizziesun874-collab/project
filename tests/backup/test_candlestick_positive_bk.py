"""
Candlestick API 正向测试用例
测试正常业务流程和有效参数
"""
import pytest
import allure

from utils.helpers import calculate_response_size, format_timestamp


@allure.feature("Candlestick API")
@allure.story("正向测试")
class TestCandlestickPositive:
    """Candlestick API 正向测试类"""

    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("测试获取 BTC_USDT 1小时 K线数据")
    @allure.description("验证能够成功获取 BTC_USDT 交易对的 1小时 K线数据")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_btc_1h_candlestick(self, api_client, validator, test_logger, save_response,positive_case):
        """
        测试用例：TC_001
        描述：获取 BTC_USDT 1小时 K线数据（最近100条）
        """
        # 准备测试数据(改进前版本实现)
        #test_case = CandlestickTestData.POSITIVE_TEST_CASES[0]

        #使用 positive_case fixture 获取数据
        test_case = positive_case("TC_POS_001")
        params = test_case["params"]

        test_logger.info(f"Test Case ID: {test_case['case_id']}")
        test_logger.info(f"Description: {test_case['description']}")
        test_logger.info(f"Request Params: {params}")

        # 步骤1：发送 API 请求
        with allure.step("发送 API 请求"):
            response_data = api_client.get_candlestick(params)
            test_logger.info(f"Response Status Code: {response_data['status_code']}")
            test_logger.info(f"Response Time: {response_data['response_time']:.2f}ms")
        test_logger.info(f"{response_data}")
        # 保存响应数据
        save_response(response_data, "btc_1h")

        # 步骤2：验证状态码
        with allure.step("验证 HTTP 状态码"):
            assert response_data["status_code"] == 200, \
                f"Expected status code 200, got {response_data['status_code']}"
            test_logger.info("✅ Status code validation passed")

        # 步骤3：验证响应结构
        with allure.step("验证响应数据结构"):
            response = response_data["response"]
            is_valid, errors = validator.validate_response_structure(response)
            assert is_valid, f"Response structure invalid: {errors}"
            test_logger.info("✅ Response structure validation passed")

        # 步骤4：验证交易对名称
        with allure.step("验证交易对名称"):
            is_valid, error = validator.validate_instrument_name(
                response,
                params["instrument_name"]
            )
            assert is_valid, error
            test_logger.info(f"✅ Instrument name validated: {params['instrument_name']}")

        # 步骤5：验证时间周期
        with allure.step("验证时间周期"):
            is_valid, error = validator.validate_timeframe(
                response,
                params["timeframe"]
            )
            assert is_valid, error
            test_logger.info(f"✅ Timeframe validated: {params['timeframe']}")

        # 步骤6：验证数据数量
        with allure.step("验证数据数量"):
            data = response["result"]["data"]
            assert len(data) > 0, "No candlestick data returned"
            assert len(data) <= params["count"], \
                f"Expected max {params['count']} data points, got {len(data)}"
            test_logger.info(f"✅ Data count validated: {len(data)} records")

        # 步骤7：验证 K线数据业务逻辑
        with allure.step("验证 K线数据业务逻辑"):
            is_valid, errors = validator.validate_candlestick_data(data)
            assert is_valid, f"Candlestick data validation failed: {errors}"
            test_logger.info("✅ Candlestick data validation passed")

        # 添加 Allure 附件
        allure.attach(
            str(params),
            name="Request Parameters",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            str(response),
            name="Response Data",
            attachment_type=allure.attachment_type.JSON
        )

    @pytest.mark.positive
    @allure.title("测试获取 ETH_USDT 5分钟 K线数据（指定时间范围）")
    @allure.description("验证能够获取指定时间范围的 ETH_USDT 5分钟 K线数据")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_eth_5m_with_time_range(self, api_client, validator, test_logger, save_response,positive_case):
        """
        测试用例：TC_002
        描述：获取 ETH_USDT 5分钟 K线数据（指定时间范围）
        """
        # 准备测试数据
        #test_case = CandlestickTestData.POSITIVE_TEST_CASES[1]
        test_case = positive_case("TC_POS_002")
        params = test_case["params"]

        test_logger.info(f"Test Case ID: {test_case['case_id']}")
        test_logger.info(f"Description: {test_case['description']}")

        # 格式化时间戳用于日志
        start_time_str = format_timestamp(params["start_ts"])
        end_time_str = format_timestamp(params["end_ts"])
        test_logger.info(f"Time Range: {start_time_str} to {end_time_str}")

        # 发送请求
        with allure.step("发送 API 请求"):
            response_data = api_client.get_candlestick(params)

        save_response(response_data, "eth_5m_time_range")

        # 验证响应
        with allure.step("验证响应"):
            assert response_data["status_code"] == 200
            response = response_data["response"]

            # 验证结构
            is_valid, errors = validator.validate_response_structure(response)
            assert is_valid, f"Response structure invalid: {errors}"

            # 验证数据
            data = response["result"]["data"]
            assert len(data) > 0, "No data returned for specified time range"

            # 验证时间戳在指定范围内
            for candle in data:
                timestamp = candle["t"]
                assert params["start_ts"] <= timestamp <= params["end_ts"], \
                    f"Timestamp {timestamp} out of range [{params['start_ts']}, {params['end_ts']}]"

            test_logger.info(f"✅ Retrieved {len(data)} candlesticks within time range")



    @pytest.mark.positive
    @allure.title("测试获取最小数量 K线（count=1）")
    @allure.description("验证 count=1 时能够正确返回1条数据")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_minimum_count_candlestick(self, api_client, validator, test_logger, save_response):
        """
        测试用例：TC_004
        描述：获取最小数量 K线（count=1）
        """
        test_case = CandlestickTestData.POSITIVE_TEST_CASES[3]
        params = test_case["params"]

        test_logger.info(f"Test Case ID: {test_case['case_id']}")
        test_logger.info(f"Testing minimum count: {params['count']}")

        # 发送请求
        response_data = api_client.get_candlestick(params)
        save_response(response_data, "min_count")

        # 验证
        assert response_data["status_code"] == 200
        response = response_data["response"]

        data = response["result"]["data"]

        # 验证数量
        with allure.step("验证返回数据数量为1"):
            assert len(data) == 1, f"Expected 1 data point, got {len(data)}"
            test_logger.info("✅ Exactly 1 candlestick returned")

        # 验证数据完整性
        candle = data[0]
        for field in ExpectedDataStructure.CANDLESTICK_FIELDS:
            assert field in candle, f"Missing field: {field}"
            assert candle[field] is not None, f"Field {field} is None"

        test_logger.info("✅ Candlestick data complete")

    @pytest.mark.positive
    @allure.title("测试获取最大数量 K线（count=300）")
    @allure.description("验证 count=300 时能够正确返回数据")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_maximum_count_candlestick(self, api_client, validator, test_logger, save_response):
        """
        测试用例：TC_005
        描述：获取最大数量 K线（count=300）
        """
        test_case = CandlestickTestData.POSITIVE_TEST_CASES[4]
        params = test_case["params"]

        test_logger.info(f"Test Case ID: {test_case['case_id']}")
        test_logger.info(f"Testing maximum count: {params['count']}")

        # 发送请求
        response_data = api_client.get_candlestick(params)
        save_response(response_data, "max_count")

        # 验证
        assert response_data["status_code"] == 200
        response = response_data["response"]

        data = response["result"]["data"]

        # 验证数量不超过最大值
        with allure.step(f"验证返回数据数量不超过 {params['count']}"):
            assert len(data) <= params["count"], \
                f"Expected max {params['count']} data points, got {len(data)}"
            test_logger.info(f"✅ Returned {len(data)} candlesticks (≤ {params['count']})")

        # 验证所有数据的完整性
        is_valid, errors = validator.validate_candlestick_data(data)
        assert is_valid, errors

        # 计算响应大小
        response_size = calculate_response_size(response_data["response"])
        test_logger.info(f"Response size: {response_size / 1024:.2f} KB")

    #验证多个不同交易对都能正常获取数据
    @pytest.mark.positive
    @pytest.mark.parametrize("instrument", [
        "BTC_USDT",
        "ETH_USDT",
        "CRO_USDT"
    ])
    @allure.title("测试多个交易对的 K线数据获取")
    @allure.description("参数化测试：验证多个不同交易对都能正常获取数据")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_instruments(self, api_client, validator, test_logger,
                                  save_response, instrument):
        """
        测试用例：TC_006
        描述：测试多个交易对（参数化）
        """
        params = {
            "instrument_name": instrument,
            "timeframe": "1h",
            "count": 50
        }

        test_logger.info(f"Testing instrument: {instrument}")

        # 发送请求
        response_data = api_client.get_candlestick(params)
        save_response(response_data, f"multi_{instrument}")

        # 验证
        assert response_data["status_code"] == 200
        response = response_data["response"]

        # 验证交易对名称
        actual_instrument = response["result"]["instrument_name"]
        assert actual_instrument == instrument, \
            f"Expected {instrument}, got {actual_instrument}"

        # 验证数据
        data = response["result"]["data"]
        assert len(data) > 0, f"No data returned for {instrument}"

        is_valid, errors = validator.validate_candlestick_data(data)
        assert is_valid, errors

        test_logger.info(f"✅ {instrument}: {len(data)} candlesticks validated")

