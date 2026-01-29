"""
api/websocket_client.py
WebSocket 客户端（适配 Crypto.com）
"""
import asyncio
import json
import websockets
from typing import Optional, Dict, Any, List
import logging


class WebSocketClient:
    """WebSocket 客户端"""

    def __init__(self, ws_url: str, timeout: int = 30):
        """
        初始化 WebSocket 客户端

        Args:
            ws_url: WebSocket URL
            timeout: 超时时间（秒）
        """
        self.ws_url = ws_url
        self.timeout = timeout
        self.ws = None
        self.request_id = 0
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
    async def connect(self) -> bool:
        """
        连接 WebSocket

        Returns:
            bool: 连接是否成功
        """
        try:
            self.logger.info(f"正在连接 WebSocket: {self.ws_url}")
            self.logger.info(f"超时设置: {self.timeout}秒")

            self.ws = await asyncio.wait_for(
                websockets.connect(
                    self.ws_url,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10
                ),
                timeout=self.timeout
            )


            self.logger.info("✅ WebSocket 连接成功")
            self.logger.info(f"连接状态: open={not self.ws.closed}")
            return True
        except Exception as e:
            self.logger.info(f"❌ WebSocket 连接失败: {type(e).__name__}: {e}")
            self.logger.info(f"URL: {self.ws_url}")
            return False
        # except asyncio.TimeoutError:
        #     self.logger.error(f"❌ WebSocket 连接超时（超时时间: {self.timeout}秒）")
        #     self.logger.error(f"URL: {self.ws_url}")
        #     return False
        # except Exception as e:
        #     self.logger.error(f"❌ WebSocket 连接失败: {type(e).__name__}: {e}")
        #     self.logger.error(f"URL: {self.ws_url}")
        #     return False

    async def disconnect(self):
        """断开 WebSocket 连接"""
        if self.ws:
            try:
                await self.ws.close()
                self.logger.info("WebSocket 已断开")
            except Exception as e:
                self.logger.error(f"断开 WebSocket 时发生错误: {e}")

    async def is_connected(self) -> bool:
        """
        检查连接状态

        Returns:
            bool: 是否已连接
        """
        connected = self.ws is not None and not self.ws.closed
        return connected

    def _get_next_id(self) -> int:
        """获取下一个请求 ID"""
        self.request_id += 1
        return self.request_id

    async def send_message(self, message: Dict[str, Any]) -> bool:
        """
        发送消息

        Args:
            message: 要发送的消息

        Returns:
            bool: 发送是否成功
        """
        if not await self.is_connected():
            self.logger.error("WebSocket 未连接，无法发送消息")
            return False

        try:
            message_str = json.dumps(message)
            self.logger.info(f"📤 发送消息: {message_str}")
            await self.ws.send(message_str)
            self.logger.info("✅ 消息发送成功")
            return True
        except Exception as e:
            self.logger.error(f"❌ 发送消息失败: {type(e).__name__}: {e}")
            return False

    async def receive_message(self, timeout: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        接收 WebSocket 消息

        Args:
            timeout: 超时时间（秒），None 表示使用默认超时

        Returns:
            Dict: 解析后的消息，如果超时或连接关闭则返回 None
        """
        if self.ws is None:
            self.logger.error("❌ WebSocket 未连接")
            return None

        timeout_value = timeout if timeout is not None else self.timeout

        try:
            self.logger.info(f"⏳ 等待接收消息（超时: {timeout_value}秒）...")

            # 接收消息
            message = await asyncio.wait_for(
                self.ws.recv(),
                timeout=timeout_value
            )

            # 打印原始消息（完整）
            self.logger.info(f"📥 收到原始消息（长度: {len(message)}）: {message}")

            # 解析 JSON
            try:
                parsed = json.loads(message)
                self.logger.info(f"✅ 解析消息成功")

                # 打印解析后的消息结构（用于调试）
                self.logger.info(f"📋 消息结构: {list(parsed.keys())}")

                # 如果有 result 字段，打印其结构
                if "result" in parsed:
                    self.logger.info(f"📋 result 结构: {list(parsed['result'].keys())}")

                    # 如果有 data 字段，打印数据条数
                    if "data" in parsed["result"]:
                        data = parsed["result"]["data"]
                        self.logger.info(f"📋 data 条数: {len(data)}")

                        # 打印第一条数据的结构
                        if len(data) > 0:
                            self.logger.info(f"📋 data[0] 结构: {list(data[0].keys())}")

                            # 检查是否有 asks 和 bids
                            if "asks" in data[0]:
                                self.logger.info(f"📋 asks 数量: {len(data[0]['asks'])}")
                            if "bids" in data[0]:
                                self.logger.info(f"📋 bids 数量: {len(data[0]['bids'])}")

                return parsed

            except json.JSONDecodeError as e:
                self.logger.error(f"❌ JSON 解析失败: {e}")
                self.logger.error(f"原始消息: {message}")
                return None

        except asyncio.TimeoutError:
            self.logger.warning(f"⏰ 接收消息超时（{timeout_value}秒）")
            return None

        except websockets.exceptions.ConnectionClosed as e:
            self.logger.error(f"❌ 连接已关闭: {e}")
            self.ws = None
            return None

        except Exception as e:
            self.logger.error(f"❌ 接收消息时发生错误: {type(e).__name__}: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None

    async def subscribe(
            self,
            channels: List[str],
            timeout: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        订阅频道（Crypto.com Exchange 格式）

        根据官方文档，订阅成功后会收到：
        1. 订阅确认: {"id": 1, "method": "subscribe", "code": 0}
        2. 数据推送: {"method": "subscribe", "result": {...}, "code": 0}

        Args:
            channels: 要订阅的频道列表
            timeout: 超时时间（秒）

        Returns:
            Dict: 订阅确认响应（仅包含 id, method, code）
        """
        if not await self.is_connected():
            self.logger.error("❌ WebSocket 未连接，无法订阅")
            return None

        request_id = self._get_next_id()

        message = {
            "id": request_id,
            "method": "subscribe",
            "params": {
                "channels": channels
            }
        }

        self.logger.info("=" * 60)
        self.logger.info(f"📢 开始订阅")
        self.logger.info(f"频道: {channels}")
        self.logger.info(f"请求 ID: {request_id}")
        self.logger.info("=" * 60)

        # 发送订阅请求
        if not await self.send_message(message):
            self.logger.error("❌ 发送订阅请求失败")
            return None

        # 等待订阅确认响应
        self.logger.info("⏳ 等待订阅确认响应...")
        timeout_value = timeout if timeout is not None else self.timeout

        try:
            response = await self.receive_message(timeout=timeout_value)

            if response is None:
                self.logger.error("❌ 未收到订阅响应")
                return None

            # 检查是否是订阅确认响应（匹配 request_id）
            if response.get("id") == request_id and response.get("method") == "subscribe":
                code = response.get("code", -1)

                if code == 0:
                    self.logger.info("=" * 60)
                    self.logger.info("✅ 订阅确认成功")
                    self.logger.info("=" * 60)
                    # 处理消息接收
                    while True:
                        message = await self.receive_message(timeout=10)

                        if message is None:
                            continue  # 如果没有消息，继续循环

                        # 检查是否是心跳消息
                        if "method" in message and message["method"] == "public/heartbeat":
                            await self.send_message({
                                "id": message.get("id"),
                                "method": "public/respond-heartbeat"
                            })
                            continue

                        # 检查是否是订单簿数据推送
                        if "result" in message:
                            result = message["result"]
                            if "data" in result:
                                # 处理订单簿数据
                                self.handle_order_book_data(result["data"])
                    return response
                else:
                    error_msg = response.get("message", "未知错误")
                    self.logger.error(f"❌ 订阅失败: {error_msg} (code: {code})")
                    return response
            else:
                self.logger.warning(f"⚠️  收到的不是预期的订阅确认响应: {response}")
                return response

        except Exception as e:
            self.logger.error(f"❌ 订阅过程发生错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None

    def handle_order_book_data(self, data):
        for entry in data:
            bids = entry.get("bids", [])
            asks = entry.get("asks", [])
            timestamp = entry.get("t", None)

            # 打印或处理 bids 和 asks
            print("Bids:", bids)
            print("Asks:", asks)
            print("Timestamp:", timestamp)
            if not bids and not asks:
                print("⚠️ 当前没有可用的买单和卖单数据")

    async def unsubscribe(
            self,
            channels: List[str],
            timeout: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        取消订阅频道

        Args:
            channels: 要取消订阅的频道列表
            timeout: 超时时间（秒）

        Returns:
            Dict: 取消订阅响应，如果失败则返回 None
        """
        if not await self.is_connected():
            self.logger.error("WebSocket 未连接，无法取消订阅")
            return None

        request_id = self._get_next_id()

        message = {
            "id": request_id,
            "method": "unsubscribe",
            "params": {
                "channels": channels
            }
        }

        self.logger.info(f"取消订阅频道: {channels}")

        # 发送取消订阅请求
        send_success = await self.send_message(message)
        if not send_success:
            self.logger.error("发送取消订阅请求失败")
            return None

        # 等待响应
        self.logger.info("等待取消订阅响应...")
        timeout_value = timeout if timeout is not None else self.timeout

        try:
            max_attempts = 5
            for attempt in range(max_attempts):
                response = await self.receive_message(timeout=timeout_value)

                if response is None:
                    continue

                if "id" in response and response["id"] == request_id:
                    self.logger.info(f"收到取消订阅响应: {response}")
                    return response

            return None

        except Exception as e:
            self.logger.error(f"等待取消订阅响应时发生错误: {e}")
            return None