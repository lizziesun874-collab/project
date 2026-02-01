"""
Pytest 配置和 Fixtures
提供测试所需的通用 fixture 和钩子函数
"""
import pytest
import logging
import os
import json
from datetime import datetime
from typing import Dict, Any
from utils.api_client import APIClient
from utils.validators import ResponseValidator, CandlestickValidator
from utils.helpers import save_response_to_file
from config.config import Config
from data.test_data_loader import TestDataLoader
from utils.ws_client import WebSocketClient
from utils.ws_validators import WebSocketValidator


# ============================================================================
# Session 级别 Fixtures（整个测试会话只创建一次）
# ============================================================================

@pytest.fixture(scope="session")
def api_client():
    """
    API 客户端 Fixture（会话级别）

    整个测试会话共享同一个客户端实例，提高性能
    """
    client = APIClient()
    yield client
    client.close()

# ==================== WebSocket Client ====================
@pytest.fixture(scope="function")
async def ws_client(test_logger):
    """    WebSocket 客户端 Fixture（异步）    自动连接和断开    """
    test_logger.info("=" * 80)
    test_logger.info("🔧 初始化 WebSocket 客户端")
    test_logger.info("=" * 80)
    # 创建客户端
    client = WebSocketClient(ws_url=Config.WS_URL, timeout=Config.WS_TIMEOUT)
    test_logger.info(f"WebSocket URL: {Config.WS_URL}")
    test_logger.info(f"超时设置: {Config.WS_TIMEOUT}秒")
    # 连接
    test_logger.info("正在连接 WebSocket...")
    connected = await client.connect()
    if not connected:
        test_logger.error("=" * 80)
        test_logger.error("❌ WebSocket 连接失败")
        test_logger.error("=" * 80)
        test_logger.error("可能的原因:")
        test_logger.error("1. 网络连接问题")
        test_logger.error("2. WebSocket URL 不正确")
        test_logger.error("3. 防火墙阻止连接")
        test_logger.error("4. 服务器不可用")
        test_logger.error("=" * 80)
        test_logger.error(f"当前 URL: {Config.WS_URL}")
        test_logger.error("=" * 80)
        pytest.fail(f"WebSocket 连接失败，请检查配置和网络: {Config.WS_URL}")
    test_logger.info("=" * 80)
    test_logger.info("✅ WebSocket 连接成功")
    test_logger.info("=" * 80)
    # 验证连接状态
    is_connected = await client.is_connected()
    test_logger.info(f"连接状态验证: {is_connected}")
    yield client
    # 断开连接
    try:
        test_logger.info("=" * 80)
        test_logger.info("正在断开 WebSocket 连接...")
        await client.disconnect()
        test_logger.info("✅ WebSocket 已断开")
        test_logger.info("=" * 80)
    except Exception as e:
        test_logger.error(f"❌ 断开连接时发生错误: {e}")

@pytest.fixture(scope="function")
def ws_client_sync(test_logger):
    """同步方式的 WebSocket 客户端 fixture（用于同步测试）"""
    def _create_client():
        return WebSocketClient(ws_url=Config.WS_URL, timeout=Config.WS_TIMEOUT)
    return _create_client

@pytest.fixture(scope="function")
def validator():
    """验证器 Fixture（支持 REST 和 WebSocket）"""
    class ValidatorWrapper:
        def __init__(self):
            self.candlestick = CandlestickValidator()
            self.websocket = WebSocketValidator()

        def __getattr__(self, name):
             if hasattr(self.websocket, name):
                 return getattr(self.websocket, name)
             elif hasattr(self.candlestick, name):
                 return getattr(self.candlestick, name)
             else:
                 raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    return ValidatorWrapper()


@pytest.fixture(scope="session")
def test_config():
    """
    测试配置 Fixture（会话级别）

    Returns:
        dict: 测试配置信息
    """
    return {
        "base_url": Config.BASE_URL,
        "timeout": Config.TIMEOUT,
        "max_retries": Config.MAX_RETRIES,
        "environment": Config.CURRENT_ENV.value
    }


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    设置测试环境（会话级别，自动执行）

    在所有测试开始前执行，测试结束后清理
    """
    # 创建必要的目录
    directories = [
        "reports",
        "reports/logs",
        "reports/responses",
        "reports/screenshots",
        "reports/coverage"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("\n" + "=" * 80)
    print("🚀 Test Environment Setup")
    print("=" * 80)
    print(f"Base URL: {Config.BASE_URL}")
    print(f"Environment: {Config.CURRENT_ENV.value}")
    print(f"Timeout: {Config.TIMEOUT}s")
    print("=" * 80 + "\n")

    yield

    # 测试结束后的清理工作
    print("\n" + "=" * 80)
    print("✅ Test Environment Teardown")
    print("=" * 80 + "\n")

@pytest.fixture(scope="session")
def test_data_loader():
    return TestDataLoader

@pytest.fixture(scope="session")
def get_test_case():
    def _get_case(case_id: str, case_type: str = "positive"):
        return TestDataLoader.get_case(case_id, case_type)
    return _get_case

@pytest.fixture(scope="session")
def positive_case():
    """    正向测试用例获取器 - session 级别        ✅ scope="session": 整个测试会话只创建一次        Usage:        def test_something(positive_case):            test_data = positive_case("TC_POS_001")    """
    def _get_case(case_id: str):
        return TestDataLoader.get_case(case_id, "positive")
    return _get_case

@pytest.fixture(scope="session")
def performance_case():
    """    性能测试用例获取器 - session 级别        ✅ scope="session": 整个测试会话只创建一次        Usage:        def test_something(performance_case):            test_data = performance_case("TC_PERF_001")    """
    def _get_case(case_id: str):
        return TestDataLoader.get_case(case_id, "performance")
    return _get_case

@pytest.fixture(scope="function")
def orderbook_case(request):
    """WebSocket 订单簿测试用例 Fixture"""
    from data import TestDataLoader
    case_id = request.param if hasattr(request, 'param') else "TC_BOOK_001"
    return TestDataLoader.ws.get_case(case_id, "orderbook")

@pytest.fixture(scope="function")
def ws_test_case(request):
    """WebSocket 通用测试用例 Fixture"""
    from data import TestDataLoader
    # 从 request.param 获取参数
    if hasattr(request, 'param'):
        if isinstance(request.param, dict):
            case_id = request.param.get("case_id", "TC_BOOK_001")
            case_type = request.param.get("case_type", "orderbook")
        else:
            case_id = request.param
            case_type = "orderbook"
    else:
        case_id = "TC_BOOK_001"
        case_type = "orderbook"
    return TestDataLoader.ws.get_case(case_id, case_type)



# ============================================================================
# Function 级别 Fixtures（每个测试函数创建一次）
# ============================================================================

@pytest.fixture(scope="function")
def test_logger(request):
    """
    测试日志 Fixture（函数级别）

    为每个测试函数创建独立的日志记录器

    Args:
        request: pytest 内置 fixture，提供测试上下文信息
    """
    logger = logging.getLogger(request.node.name)
    logger.setLevel(logging.DEBUG)

    # 创建日志目录
    log_dir = "reports/logs"
    os.makedirs(log_dir, exist_ok=True)

    # 创建文件处理器
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{request.node.name}_{timestamp}.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 记录测试开始
    logger.info(f"{'=' * 60}")
    logger.info(f"Test Started: {request.node.name}")
    logger.info(f"{'=' * 60}")

    yield logger

    # 记录测试结束
    logger.info(f"{'=' * 60}")
    logger.info(f"Test Finished: {request.node.name}")
    logger.info(f"{'=' * 60}")

    # 清理处理器
    file_handler.close()
    console_handler.close()
    logger.removeHandler(file_handler)
    logger.removeHandler(console_handler)


#@pytest.fixture(scope="function")
# def save_response(request):
#     """
#     保存响应数据 Fixture（函数级别）
#
#     提供保存 API 响应的便捷方法
#
#     Returns:
#         function: 保存响应的函数
#     """
#
#     def _save(response_data: Dict[str, Any], suffix: str = ""):
#         """
#         保存响应数据
#
#         Args:
#             response_响应数据
#             suffix: 文件名后缀
#         """
#         test_name = request.node.name
#         if suffix:
#             test_name = f"{test_name}_{suffix}"
#
#         return save_response_to_file(
#             response_data,
#             test_name,
#             directory="reports/responses"
#         )
#
#     return _save

@pytest.fixture(scope="function")
def save_response(request):
    """
    保存响应数据 Fixture (兼容 API 和 WebSocket)
    """

    def _save(data: Dict[str, Any], suffix: str = "", **kwargs):
        """
        Args:
            data: 要保存的数据
            suffix: 原始后缀
            **kwargs: 接收 case_id, step 等扩展字段
        """
        # 获取基础文件名（测试函数名）
        test_name = request.node.name

        # 扩展文件名逻辑：如果传入了 case_id 或 step，拼接到文件名中
        case_id = kwargs.get("case_id", "")
        step = kwargs.get("step", "")

        parts = [test_name]
        if case_id: parts.append(str(case_id))
        if step: parts.append(str(step))
        if suffix: parts.append(suffix)

        final_filename = "_".join(parts)

        # 调用你现有的保存函数
        return save_response_to_file(
            data,
            final_filename,
            directory="reports/responses"
        )

    return _save


@pytest.fixture(scope="function")
def test_data_collector(request):
    """
    测试数据收集器 Fixture（函数级别）

    收集测试执行过程中的数据，用于生成报告
    """
    collector = {
        "test_name": request.node.name,
        "start_time": datetime.now(),
        "requests": [],
        "responses": [],
        "assertions": [],
        "errors": []
    }

    yield collector

    # 测试结束后保存收集的数据
    collector["end_time"] = datetime.now()
    collector["duration"] = (
            collector["end_time"] - collector["start_time"]
    ).total_seconds()

    # 保存到文件
    data_file = os.path.join(
        "reports",
        f"{request.node.name}_data.json"
    )
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(
            collector,
            f,
            indent=2,
            ensure_ascii=False,
            default=str  # 处理 datetime 对象
        )


# ============================================================================
# Pytest 钩子函数
# ============================================================================

def pytest_configure(config):
    """
    Pytest 配置钩子

    在测试开始前配置 pytest
    """
    # 注册自定义标记
    config.addinivalue_line(
        "markers",
        "smoke: 冒烟测试，快速验证核心功能"
    )
    config.addinivalue_line(
        "markers",
        "positive: 正向测试，验证正常业务流程"
    )
    config.addinivalue_line(
        "markers",
        "negative: 负向测试，验证异常处理"
    )
    config.addinivalue_line(
        "markers",
        "boundary: 边界测试，验证边界条件"
    )
    config.addinivalue_line(
        "markers",
        "performance: 性能测试，验证响应时间和并发"
    )
    config.addinivalue_line(
        "markers",
        "slow: 慢速测试，执行时间较长"
    )
    config.addinivalue_line(
        "markers",
        "critical: 关键测试，必须通过"
    )
    config.addinivalue_line("markers", "websocket: WebSocket 测试"
                            )
    config.addinivalue_line("markers", "rest: REST API 测试")
    config.addinivalue_line("markers", "orderbook: 订单簿测试")


def pytest_collection_modifyitems(config, items):
    """
    修改收集到的测试项

    为测试添加标记或修改测试顺序
    """
    # 为测试添加 Allure 标签
    for item in items:
        # 根据测试文件名添加 feature 标签
        if "positive" in item.nodeid:
            item.add_marker(pytest.mark.allure_label(item.nodeid, label_type="feature", value="Positive Tests"))
        elif "negative" in item.nodeid:
            item.add_marker(pytest.mark.allure_label(item.nodeid, label_type="feature", value="Negative Tests"))
        elif "boundary" in item.nodeid:
            #item.add_marker(pytest.mark.allure_label("feature", "Boundary Tests"))
            item.add_marker(pytest.mark.allure_label(item.nodeid, label_type="feature", value="Boundary Tests"))
        elif "performance" in item.nodeid:
            #item.add_marker(pytest.mark.allure_label("feature", "Performance Tests"))
            item.add_marker(pytest.mark.allure_label(item.nodeid, label_type="feature", value="Performance Tests"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    生成测试报告钩子

    在每个测试阶段（setup, call, teardown）后调用
    """
    outcome = yield
    report = outcome.get_result()

    # 只处理测试执行阶段
    if report.when == "call":
        # 将测试结果附加到 item 对象
        setattr(item, f"report_{report.when}", report)

        # 如果测试失败，记录详细信息
        if report.failed:
            # 获取失败信息
            error_message = str(report.longrepr)

            # 保存失败信息到文件
            failure_dir = "reports/failures"
            os.makedirs(failure_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            failure_file = os.path.join(
                failure_dir,
                f"{item.name}_{timestamp}.txt"
            )

            with open(failure_file, 'w', encoding='utf-8') as f:
                f.write(f"Test: {item.name}\n")
                f.write(f"Time: {datetime.now()}\n")
                f.write(f"{'=' * 80}\n")
                f.write(error_message)


@pytest.fixture(scope="function", autouse=True)
def test_wrapper(request, test_logger):
    """
    测试包装器（自动执行）

    在每个测试前后执行，记录测试信息
    """
    test_name = request.node.name
    test_logger.info(f"▶️  Starting test: {test_name}")

    start_time = datetime.now()

    yield

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # 获取测试结果
    if hasattr(request.node, 'report_call'):
        result = request.node.report_call
        if result.passed:
            test_logger.info(f"✅ Test PASSED: {test_name} (Duration: {duration:.2f}s)")
        elif result.failed:
            test_logger.error(f"❌ Test FAILED: {test_name} (Duration: {duration:.2f}s)")
        elif result.skipped:
            test_logger.warning(f"⏭️  Test SKIPPED: {test_name}")
        else:
            test_logger.info(f"⏹️  Test finished: {test_name} (Duration: {duration:.2f}s)")

@pytest.fixture(scope="session")
def valid_instruments():
    """有效的交易对列表"""
    return ["BTC_USDT", "ETH_USDT", "CRO_USDT", "DOGE_USDT", "SOL_USDT"]
@pytest.fixture(scope="session")
def valid_timeframes():
    """有效的时间周期列表"""
    return ["1m", "5m", "15m", "30m", "1h", "4h", "6h", "12h", "1D", "7D", "14D", "1M"]
@pytest.fixture(scope="function")
def sample_candlestick_response():
    """示例 K线响应数据"""
    return {"code": 0,
            "method": "public/get-candlestick",
            "result": {"instrument_name": "BTC_USDT", "interval": "1h", "data": [
                {"t": 1705315200000, "o": 42500.5, "h": 42800.0, "l": 42300.0, "c": 42650.0, "v": 1234.56},
                {"t": 1705318800000, "o": 42650.0, "h": 42900.0, "l": 42600.0, "c": 42750.0, "v": 2345.67}]}}
