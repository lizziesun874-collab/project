"""
utils/ws_validators.py
WebSocket 数据验证器（适配 Crypto.com Exchange）
"""
from typing import Dict, Any, List, Optional
import logging


class WebSocketValidator:
    """WebSocket 数据验证器"""

    def __init__(self):
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

    # ==================== 订阅相关验证 ====================

    def validate_subscription_response(
            self,
            response: Dict[str, Any],
            expected_channels: Optional[List[str]] = None
    ) -> bool:
        """
        验证订阅响应（Crypto.com 格式）

        实际响应格式:
        成功: {"id": 1, "method": "subscribe", "code": 0, "channel": "book.BTCUSD-PERP.10"}
        失败: {"id": 1, "method": "subscribe", "code": 10004, "message": "INVALID_REQUEST"}

        Args:
            response: 订阅响应消息
            expected_channels: 预期的频道列表（可选）

        Returns:
            bool: 验证是否通过

        Raises:
            AssertionError: 验证失败时抛出
        """
        try:
            # 首先检查响应是否为空
            assert response is not None, "订阅响应为空（None）"
            assert isinstance(response, dict), f"订阅响应应该是字典类型（实际类型: {type(response)}）"

            self.logger.info(f"开始验证订阅响应: {response}")

            # Crypto.com 响应格式验证
            # 必需字段: id, method, code
            assert "id" in response, "缺少 id 字段"
            assert "method" in response, "缺少 method 字段"
            assert "code" in response, "缺少 code 字段"

            request_id = response["id"]
            method = response["method"]
            code = response["code"]

            assert method == "subscribe", f"method 应该是 'subscribe'（实际: {method}）"

            self.logger.info(f"请求 ID: {request_id}, 方法: {method}, 响应码: {code}")

            # 验证响应码
            if code == 0:
                # 订阅成功
                self.logger.info(f"✅ 订阅成功（code=0）")

                # 验证频道字段（可能是 channel 或 channels）
                actual_channel = response.get("channel")

                if actual_channel:
                    self.logger.info(f"订阅频道: {actual_channel}")

                    # 如果指定了预期频道，验证是否匹配
                    if expected_channels:
                        assert actual_channel in expected_channels, \
                            f"订阅频道不匹配（预期之一: {expected_channels}, 实际: {actual_channel}）"

                        self.logger.info(f"✅ 频道验证通过: {actual_channel}")
                else:
                    self.logger.warning("响应中没有 channel 字段")

                return True

            else:
                # 订阅失败
                error_msg = response.get("message", "未知错误")
                error_text = f"订阅失败: {error_msg} (code: {code})"
                self.logger.error(f"❌ {error_text}")
                raise AssertionError(error_text)

        except AssertionError as e:
            self.logger.error(f"❌ 订阅响应验证失败: {e}")
            self.logger.error(f"响应内容: {response}")
            raise



    def validate_book_push_message(
            self,
            message: Dict[str, Any],
            expected_subscription: str,
            expected_depth: int
    ) -> bool:
        """
        验证订单簿推送消息（Crypto.com 格式）

        推送消息格式（根据官方文档）:
        {
          "method": "subscribe",
          "result": {
            "instrument_name": "ETH_CRO",
            "subscription": "book.ETH_CRO.10",
            "channel": "book",
            "depth": 10,
            "data": [{
              "bids": [[price, quantity, number_of_orders], ...],
              "asks": [[price, quantity, number_of_orders], ...],
              "t": timestamp
            }]
          },
          "code": 0
        }

        Args:
            message: 推送消息
            expected_subscription: 预期的订阅频道（如 "book.BTCUSD-PERP.10"）
            expected_depth: 预期的深度

        Returns:
            bool: 验证是否通过
        """
        try:
            assert message is not None, "推送消息为空"
            assert isinstance(message, dict), f"推送消息应该是字典（实际: {type(message)}）"

            self.logger.info(f"验证订单簿推送消息")

            # 必需字段
            assert "method" in message, "缺少 method 字段"
            assert "result" in message, "缺少 result 字段"
            assert "code" in message, "缺少 code 字段"

            method = message["method"]
            code = message["code"]
            result = message["result"]

            assert method == "subscribe", f"method 应该是 'subscribe'（实际: {method}）"
            assert code == 0, f"code 应该是 0（实际: {code}）"
            assert isinstance(result, dict), f"result 应该是字典（实际: {type(result)}）"

            # 验证 result 字段
            assert "instrument_name" in result, "result 缺少 instrument_name 字段"
            assert "subscription" in result, "result 缺少 subscription 字段"
            assert "channel" in result, "result 缺少 channel 字段"
            assert "depth" in result, "result 缺少 depth 字段"
            assert "data" in result, "result 缺少 data 字段"

            instrument_name = result["instrument_name"]
            subscription = result["subscription"]
            channel = result["channel"]
            depth = result["depth"]
            data = result["data"]

            self.logger.info(f"合约: {instrument_name}")
            self.logger.info(f"订阅: {subscription}")
            self.logger.info(f"频道: {channel}")
            self.logger.info(f"深度: {depth}")

            # 验证字段值
            assert channel == "book", f"channel 应该是 'book'（实际: {channel}）"
            assert subscription == expected_subscription, \
                f"subscription 不匹配（预期: {expected_subscription}, 实际: {subscription}）"
            assert depth == expected_depth, \
                f"depth 不匹配（预期: {expected_depth}, 实际: {depth}）"

            # 验证 data
            assert isinstance(data, list), f"data 应该是列表（实际: {type(data)}）"
            assert len(data) > 0, "data 不应为空"

            self.logger.info("✅ 订单簿推送消息结构验证通过")
            return True

        except AssertionError as e:
            self.logger.error(f"❌ 订单簿推送消息验证失败: {e}")
            self.logger.error(f"消息内容: {message}")
            raise

    def validate_notification_message(
            self,
            message: Dict[str, Any],
            expected_channel: Optional[str] = None
    ) -> bool:
        """
        验证推送通知消息（Crypto.com 格式）

        Args:
            message: 推送消息
            expected_channel: 预期的频道（可选）

        Returns:
            bool: 验证是否通过

        Raises:
            AssertionError: 验证失败时抛出
        """
        try:
            assert message is not None, "推送消息为空（None）"
            assert isinstance(message, dict), f"推送消息应该是字典类型（实际类型: {type(message)}）"

            # 验证基础字段
            assert "method" in message, "缺少 method 字段"
            assert "result" in message, "缺少 result 字段"

            result = message["result"]
            assert isinstance(result, dict), f"result 应该是字典类型（实际类型: {type(result)}）"

            # 验证 result 中的必需字段
            assert "instrument_name" in result, "result 缺少 instrument_name 字段"
            assert "subscription" in result, "result 缺少 subscription 字段"
            assert "channel" in result, "result 缺少 channel 字段"
            assert "data" in result, "result 缺少 data 字段"

            # 验证频道
            if expected_channel:
                actual_subscription = result["subscription"]
                assert actual_subscription == expected_channel, \
                    f"频道不匹配（预期: {expected_channel}, 实际: {actual_subscription}）"

            self.logger.info(f"✅ 推送消息验证通过")
            self.logger.info(f"  - 合约: {result['instrument_name']}")
            self.logger.info(f"  - 订阅: {result['subscription']}")
            self.logger.info(f"  - 频道: {result['channel']}")

            return True

        except AssertionError as e:
            self.logger.error(f"❌ 推送消息验证失败: {e}")
            self.logger.error(f"消息内容: {message}")
            raise

    def validate_orderbook_content(self,data):
        """
        验证订单簿业务内容：价格排序、买卖盘不倒挂
        """

        if 'bids' not in data and 'result' in data:
            # 如果传入的是外层结构，深入挖掘
            actual_data_list = data.get('result', {}).get('data', [])
            if actual_data_list:
                data = actual_data_list[0]
            else:
                raise ValueError("❌ 错误: 无法解析到订单簿核心数据层级")

        bids = data.get('bids', [])  # 格式通常为 [[price, size], ...]
        asks = data.get('asks', [])

        if not bids or not asks:
            raise ValueError("❌ 错误: 买盘或卖盘数据为空")

        # 1. 提取买一和卖一
        best_bid_price = float(bids[0][0])
        best_ask_price = float(asks[0][0])

        # 2. 核心校验：买一价必须小于卖一价
        if best_bid_price >= best_ask_price:
            raise AssertionError(
                f"❌ 订单簿倒挂! 买一价({best_bid_price}) >= 卖一价({best_ask_price})"
            )
        print(f"✅ 价格交叉校验通过: {best_bid_price} < {best_ask_price}")

        # 3. 进阶校验：买盘必须降序排列
        bid_prices = [float(b[0]) for b in bids]
        if bid_prices != sorted(bid_prices, reverse=True):
            raise AssertionError("❌ 买盘价格未按降序(从高到低)排列")

        # 4. 进阶校验：卖盘必须升序排列
        ask_prices = [float(a[0]) for a in asks]
        if ask_prices != sorted(ask_prices):
            raise AssertionError("❌ 卖盘价格未按升序(从低到高)排列")

        return True

    def validate_orderbook_data(
            self,
            data:List[Dict[str, Any]],
    expected_depth: Optional[int] = None

    ) -> bool:
        """
        验证订单簿数据（Crypto.com 格式）

        Args:
            订单簿数据列表
            expected_depth: 预期的深度（可选）

        Returns:
            bool: 验证是否通过

        Raises:
            AssertionError: 验证失败时抛出
        """
        try:
            assert data is not None, "订单簿数据为空（None）"
            assert isinstance(data, list), f"订单簿数据应该是列表类型（实际类型: {type(data)}）"
            assert len(data) > 0, "订单簿数据列表为空"

            # 验证每一条订单簿数据
            for i, item in enumerate(data):
                assert isinstance(item, dict), f"订单簿数据项 {i} 应该是字典类型"

                # 验证必需字段
                assert "bids" in item, f"订单簿数据项 {i} 缺少 bids 字段"
                assert "asks" in item, f"订单簿数据项 {i} 缺少 asks 字段"
                assert "t" in item, f"订单簿数据项 {i} 缺少 t (时间戳) 字段"

                bids = item["bids"]
                asks = item["asks"]
                timestamp = item["t"]

                # 验证买单和卖单格式
                assert isinstance(bids, list), f"bids 应该是列表类型（实际类型: {type(bids)}）"
                assert isinstance(asks, list), f"asks 应该是列表类型（实际类型: {type(asks)}）"

                # 验证深度
                if expected_depth:
                    assert len(bids) <= expected_depth, \
                        f"买单深度超出预期（预期: {expected_depth}, 实际: {len(bids)}）"
                    assert len(asks) <= expected_depth, \
                        f"卖单深度超出预期（预期: {expected_depth}, 实际: {len(asks)}）"

                # 验证订单格式 [price, quantity]
                for j, bid in enumerate(bids):
                    assert isinstance(bid, list), f"买单 {j} 应该是列表格式 [price, quantity]"
                    assert len(bid) == 2, f"买单 {j} 应该包含 [price, quantity]（实际长度: {len(bid)}）"

                    price, quantity = bid
                    assert isinstance(price, (int, float, str)), \
                        f"买单 {j} 价格应该是数字或字符串（实际类型: {type(price)}）"
                    assert isinstance(quantity, (int, float, str)), \
                        f"买单 {j} 数量应该是数字或字符串（实际类型: {type(quantity)}）"

                    # 转换为浮点数验证
                    try:
                        price_float = float(price)
                        quantity_float = float(quantity)
                        assert price_float > 0, f"买单 {j} 价格应该大于 0（实际: {price_float}）"
                        assert quantity_float > 0, f"买单 {j} 数量应该大于 0（实际: {quantity_float}）"
                    except (ValueError, TypeError) as e:
                        raise AssertionError(f"买单 {j} 价格或数量无法转换为数字: {e}")

                for j, ask in enumerate(asks):
                    assert isinstance(ask, list), f"卖单 {j} 应该是列表格式 [price, quantity]"
                    assert len(ask) == 2, f"卖单 {j} 应该包含 [price, quantity]（实际长度: {len(ask)}）"

                    price, quantity = ask
                    assert isinstance(price, (int, float, str)), \
                        f"卖单 {j} 价格应该是数字或字符串（实际类型: {type(price)}）"
                    assert isinstance(quantity, (int, float, str)), \
                        f"卖单 {j} 数量应该是数字或字符串（实际类型: {type(quantity)}）"

                    # 转换为浮点数验证
                    try:
                        price_float = float(price)
                        quantity_float = float(quantity)
                        assert price_float > 0, f"卖单 {j} 价格应该大于 0（实际: {price_float}）"
                        assert quantity_float > 0, f"卖单 {j} 数量应该大于 0（实际: {quantity_float}）"
                    except (ValueError, TypeError) as e:
                        raise AssertionError(f"卖单 {j} 价格或数量无法转换为数字: {e}")

                # 验证价格排序（买单降序，卖单升序）
                if len(bids) > 1:
                    bid_prices = [float(bid[0]) for bid in bids]
                    for j in range(len(bid_prices) - 1):
                        assert bid_prices[j] >= bid_prices[j + 1], \
                            f"买单价格应该降序排列（位置 {j}: {bid_prices[j]}, 位置 {j + 1}: {bid_prices[j + 1]}）"

                if len(asks) > 1:
                    ask_prices = [float(ask[0]) for ask in asks]
                    for j in range(len(ask_prices) - 1):
                        assert ask_prices[j] <= ask_prices[j + 1], \
                            f"卖单价格应该升序排列（位置 {j}: {ask_prices[j]}, 位置 {j + 1}: {ask_prices[j + 1]}）"

                # 验证买卖价差（最高买价应该小于最低卖价）
                if len(bids) > 0 and len(asks) > 0:
                    highest_bid = float(bids[0][0])
                    lowest_ask = float(asks[0][0])
                    assert highest_bid < lowest_ask, \
                        f"最高买价应该小于最低卖价（买: {highest_bid}, 卖: {lowest_ask}）"

                # 验证时间戳
                assert isinstance(timestamp, (int, float, str)), \
                    f"时间戳应该是数字或字符串（实际类型: {type(timestamp)}）"

                try:
                    timestamp_int = int(timestamp)
                    assert timestamp_int > 0, f"时间戳应该大于 0（实际: {timestamp_int}）"
                except (ValueError, TypeError) as e:
                    raise AssertionError(f"时间戳无法转换为整数: {e}")

                self.logger.info(f"✅ 订单簿数据 {i + 1} 验证通过")
                self.logger.info(f"  - 买单数量: {len(bids)}")
                self.logger.info(f"  - 卖单数量: {len(asks)}")
                self.logger.info(f"  - 时间戳: {timestamp}")
                if len(bids) > 0:
                    self.logger.info(f"  - 最高买价: {bids[0][0]}")
                if len(asks) > 0:
                    self.logger.info(f"  - 最低卖价: {asks[0][0]}")

            self.logger.info(f"✅ 所有订单簿数据验证通过（共 {len(data)} 条）")
            return True

        except AssertionError as e:
            self.logger.error(f"❌ 订单簿数据验证失败: {e}")
            self.logger.error(f"数据内容: {data}")
            raise