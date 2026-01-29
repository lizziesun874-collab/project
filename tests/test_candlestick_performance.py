"""
tests/test_candlestick_performance.py
K线数据接口性能测试
"""

import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import allure

from utils.api_client import APIClient
from utils.test_helpers import TestHelpers

#from utils.test_helpers import basic_data_validation





class TestCandlestickPerformance:
    """K线数据接口性能测试类"""
    # ==================== 响应时间测试 ====================

    @allure.epic("Crypto API 性能测试")
    @allure.feature("响应时间测试")
    @allure.story("1小时周期小数据量响应时间")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.performance
    @pytest.mark.smoke
    def test_perf_001_response_time_1h_small(self,
            api_client,
            test_logger,
            save_response,
            performance_case):
        """TC_PERF_001: 响应时间测试（1小时周期，小数据量）"""
        #case = CASES["TC_PERF_001"]
        case = performance_case("TC_PERF_001")
        with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
            test_logger.info(f"测试用例: {case['case_id']}")
            test_logger.info(f"描述: {case['description']}")
            test_logger.info(f"请求参数: {case['params']}")

        api_params = {"instrument_name": case['params']['instrument_name'],"timeframe": case['params']['timeframe'], "count": case['params']['count']    }
        # 执行单次请求并测量响应时间
        start_time = time.time()
        response = api_client.get_candlestick(params=api_params)
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒

        # 获取实际的 API 响应数据
        response_data = response.get('response', {})
        # 保存响应数据
        save_response(response_data, "perf_001")

        data_points = 0
        if 'result' in response_data:
            result = response_data['result']
            if isinstance(result, dict) and 'data' in result:
                data_points = len(result['data'])
            elif isinstance(result, list):
                data_points = len(result)




        TestHelpers.execute_basic_test(api_client, case, save_response, test_logger)

        with allure.step("验证响应时间"):
            test_logger.info(f"响应时间: {response_time:.2f} ms")
            test_logger.info(f"最大允许响应时间: {case['expected']['max_response_time']} ms")

            # 附加性能数据到 Allure 报告
            performance_data = (
                f"响应时间: {response_time:.2f} ms\n"
                f"最大允许: {case['expected']['max_response_time']} ms\n"
                f"平均预期: {case['expected']['avg_response_time']} ms\n"
                f"数据点数量: {data_points}\n"
                f"状态: {'✓ 通过' if response_time <= case['expected']['max_response_time'] else '✗ 失败'}"
            )
            allure.attach(
                performance_data,
                name="响应时间统计",
                attachment_type=allure.attachment_type.TEXT
            )

            # 验证响应时间性能指标
            assert response_time <= case['expected']['max_response_time'], \
                f"响应时间超标: 期望 <= {case['expected']['max_response_time']} ms, 实际 {response_time:.2f} ms"

            # 记录百分位数（如果有多次测试）
            if 'performance_metrics' in case:
                metrics = case['performance_metrics']
                test_logger.info(f"性能基准 - P50: {metrics['p50']} ms, P90: {metrics['p90']} ms, "
                            f"P95: {metrics['p95']} ms, P99: {metrics['p99']} ms")

        test_logger.info(f"✓ 测试通过 - 响应时间: {response_time:.2f} ms, 数据点: {data_points}")
        #test_logger.info(f"✓ 测试通过 - 响应时间: {response_time:.2f} ms")

    # # ==================== 并发性能测试 ====================
    #
    # @allure.epic("Crypto API 性能测试")
    # @allure.feature("并发性能测试")
    # @allure.story("低并发测试（5个并发用户）")
    # @allure.severity(allure.severity_level.CRITICAL)
    # @pytest.mark.performance
    # @pytest.mark.smoke
    # def test_perf_006_concurrency_low(self):
    #     """TC_PERF_006: 低并发测试（5个并发用户）"""
    #     case = CASES["TC_PERF_006"]
    #
    #     with allure.step(f"执行测试用例: {case['case_id']} - {case['description']}"):
    #         logger.info(f"测试用例: {case['case_id']}")
    #         logger.info(f"描述: {case['description']}")
    #         logger.info(f"并发配置: {case['concurrency']}")
    #
    #         # 执行并发测试
    #         stats = self._execute_concurrent_requests(case)
    #
    #         with allure.step("验证并发测试结果"):
    #             logger.info(f"总请求数: {stats['total_requests']}")
    #             logger.info(f"成功请求数: {stats['success_count']}")
    #             logger.info(f"失败请求数: {stats['error_count']}")
    #             logger.info(f"成功率: {stats['success_rate']:.2f}%")
    #             logger.info(f"错误率: {stats['error_rate']:.2f}%")
    #
    #             # 验证成功率
    #             assert stats['success_rate'] >= case['expected']['success_rate'], \
    #                 f"成功率低于预期: 期望 >= {case['expected']['success_rate']}%, 实际 {stats['success_rate']:.2f}%"
    #
    #             # 验证错误率
    #             assert stats['error_rate'] <= case['expected']['error_rate'], \
    #                 f"错误率高于预期: 期望 <= {case['expected']['error_rate']}%, 实际 {stats['error_rate']:.2f}%"
    #
    #         with allure.step("验证响应时间统计"):
    #             if stats['response_times']:
    #                 logger.info(f"最小响应时间: {stats['min_response_time']:.2f} ms")
    #                 logger.info(f"最大响应时间: {stats['max_response_time']:.2f} ms")
    #                 logger.info(f"平均响应时间: {stats['avg_response_time']:.2f} ms")
    #                 logger.info(f"中位数响应时间: {stats['median_response_time']:.2f} ms")
    #                 logger.info(f"P50: {stats['p50']:.2f} ms")
    #                 logger.info(f"P90: {stats['p90']:.2f} ms")
    #                 logger.info(f"P95: {stats['p95']:.2f} ms")
    #                 logger.info(f"P99: {stats['p99']:.2f} ms")
    #
    #                 # 验证最大响应时间
    #                 assert stats['max_response_time'] <= case['expected']['max_response_time'], \
    #                     f"最大响应时间超标: 期望 <= {case['expected']['max_response_time']} ms, " \
    #                     f"实际 {stats['max_response_time']:.2f} ms"
    #
    #                 # 验证平均响应时间
    #                 assert stats['avg_response_time'] <= case['expected']['avg_response_time'], \
    #                     f"平均响应时间超标: 期望 <= {case['expected']['avg_response_time']} ms, " \
    #                     f"实际 {stats['avg_response_time']:.2f} ms"
    #
    #                 # 验证性能指标（百分位数）
    #                 if 'performance_metrics' in case:
    #                     metrics = case['performance_metrics']
    #
    #                     assert stats['p50'] <= metrics['p50'], \
    #                         f"P50 响应时间超标: 期望 <= {metrics['p50']} ms, 实际 {stats['p50']:.2f} ms"
    #
    #                     assert stats['p90'] <= metrics['p90'], \
    #                         f"P90 响应时间超标: 期望 <= {metrics['p90']} ms, 实际 {stats['p90']:.2f} ms"
    #
    #                     assert stats['p95'] <= metrics['p95'], \
    #                         f"P95 响应时间超标: 期望 <= {metrics['p95']} ms, 实际 {stats['p95']:.2f} ms"
    #
    #                     assert stats['p99'] <= metrics['p99'], \
    #                         f"P99 响应时间超标: 期望 <= {metrics['p99']} ms, 实际 {stats['p99']:.2f} ms"
    #
    #                 # 附加性能统计到 Allure 报告
    #                 performance_summary = (
    #                     f"并发配置:\n"
    #                     f"  - 并发用户数: {case['concurrency']['users']}\n"
    #                     f"  - 每用户请求数: {case['concurrency']['requests_per_user']}\n"
    #                     f"  - Ramp-up 时间: {case['concurrency']['ramp_up_time']} 秒\n\n"
    #                     f"请求统计:\n"
    #                     f"  - 总请求数: {stats['total_requests']}\n"
    #                     f"  - 成功请求数: {stats['success_count']}\n"
    #                     f"  - 失败请求数: {stats['error_count']}\n"
    #                     f"  - 成功率: {stats['success_rate']:.2f}%\n"
    #                     f"  - 错误率: {stats['error_rate']:.2f}%\n\n"
    #                     f"响应时间统计:\n"
    #                     f"  - 最小: {stats['min_response_time']:.2f} ms\n"
    #                     f"  - 最大: {stats['max_response_time']:.2f} ms\n"
    #                     f"  - 平均: {stats['avg_response_time']:.2f} ms\n"
    #                     f"  - 中位数: {stats['median_response_time']:.2f} ms\n\n"
    #                     f"百分位数:\n"
    #                     f"  - P50: {stats['p50']:.2f} ms\n"
    #                     f"  - P90: {stats['p90']:.2f} ms\n"
    #                     f"  - P95: {stats['p95']:.2f} ms\n"
    #                     f"  - P99: {stats['p99']:.2f} ms\n\n"
    #                     f"状态: ✓ 测试通过"
    #                 )
    #                 allure.attach(
    #                     performance_summary,
    #                     name="并发性能测试统计",
    #                     attachment_type=allure.attachment_type.TEXT
    #                 )
    #
    #         with allure.step("验证数据完整性（抽样检查）"):
    #             # 随机抽取一次请求验证数据完整性
    #             response = self.client.get_candlestick(**case['params'])
    #             if response.status_code == 200:
    #                 data = response.json()
    #                 basic_data_validation(data)
    #                 logger.info("✓ 数据完整性验证通过")
    #
    #         logger.info(f"✓ 并发测试通过 - 成功率: {stats['success_rate']:.2f}%, "
    #                     f"平均响应时间: {stats['avg_response_time']:.2f} ms")
    #
    # # ==================== 辅助方法 ====================
    #
    # def _execute_concurrent_requests(self, case: Dict[str, Any]) -> Dict[str, Any]:
    #     """
    #     执行并发请求
    #
    #     Args:
    #         case: 测试用例数据
    #
    #     Returns:
    #         性能统计数据字典，包含:
    #             - total_requests: 总请求数
    #             - success_count: 成功请求数
    #             - error_count: 失败请求数
    #             - success_rate: 成功率（百分比）
    #             - error_rate: 错误率（百分比）
    #             - response_times: 响应时间列表
    #             - min_response_time: 最小响应时间
    #             - max_response_time: 最大响应时间
    #             - avg_response_time: 平均响应时间
    #             - median_response_time: 中位数响应时间
    #             - p50, p90, p95, p99: 各百分位数响应时间
    #     """
    #     concurrency = case['concurrency']
    #     users = concurrency['users']
    #     requests_per_user = concurrency['requests_per_user']
    #     ramp_up_time = concurrency['ramp_up_time']
    #
    #     response_times = []
    #     success_count = 0
    #     error_count = 0
    #     status_codes = []
    #
    #     logger.info(f"开始并发测试: {users} 个用户, 每用户 {requests_per_user} 个请求, "
    #                 f"Ramp-up: {ramp_up_time} 秒")
    #
    #     def make_request(user_id: int, request_id: int) -> Dict[str, Any]:
    #         """
    #         执行单个请求
    #
    #         Args:
    #             user_id: 用户ID
    #             request_id: 请求ID
    #
    #         Returns:
    #             请求结