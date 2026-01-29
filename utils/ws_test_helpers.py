"""
utils/ws_test_helpers.py
WebSocket 测试辅助函数
"""
import json
import allure
from typing import Dict, Any



class WebSocketTestHelper:
    """WebSocket 测试辅助类"""

    @staticmethod
    async def execute_subscribe_test(
            ws_client,
            test_logger,
            save_response,
            case: Dict[str, Any],
            validator
    ):
        """执行订阅测试的通用流程"""
        case_id = case['case_id']
        params = case['params']
        expected = case.get('expected', {})

        # 构建订阅频道
        instrument_name = params['instrument_name']
        depth = params['depth']
        channel = f"book.{instrument_name}.{depth}"

        with allure.step(f"1. 订阅频道: {channel}"):
            test_logger.info("=" * 80)
            test_logger.info(f"📢 发送订阅请求: {channel}")
            test_logger.info("=" * 80)

            # 发送订阅请求并获取确认响应
            subscribe_confirm = await ws_client.subscribe(
                channels=[channel],
                timeout=30
            )

            assert subscribe_confirm is not None, "未收到订阅确认响应"

            test_logger.info(f"订阅确认: {subscribe_confirm}")

            # 保存订阅确认
            if save_response:
                save_response(
                    case_id=case_id,
                    step="subscribe_confirm",
                    data=subscribe_confirm
                )

            allure.attach(
                json.dumps(subscribe_confirm, indent=2, ensure_ascii=False),
                name="1. 订阅确认响应",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("2. 验证订阅确认响应"):
            validator.validate_subscription_response(subscribe_confirm)
            test_logger.info("✅ 订阅确认验证通过")

        with allure.step("3. 等待订单簿数据推送"):
            test_logger.info("=" * 80)
            test_logger.info("⏳ 等待订单簿数据推送...")
            test_logger.info("=" * 80)

            book_data = None
            max_attempts = 20

            for attempt in range(max_attempts):
                test_logger.info(f"🔍 尝试接收 ({attempt + 1}/{max_attempts})...")

                message = await ws_client.receive_message(timeout=10)

                if message is None:
                    test_logger.warning(f"⚠️  第 {attempt + 1} 次接收超时")
                    continue

                test_logger.info(f"📨 收到消息: method={message.get('method')}, "
                                 f"has_result={('result' in message)}, "
                                 f"code={message.get('code')}")

                # 处理心跳
                if message.get("method") == "public/heartbeat":
                    test_logger.info("💓 收到心跳，回复 pong")
                    await ws_client.send_message({
                        "id": message.get("id"),
                        "method": "public/respond-heartbeat"
                    })
                    continue

                # 检查是否是订单簿推送（有 result 和 data）
                if (message.get("method") == "subscribe" and
                        "result" in message and
                        isinstance(message["result"], dict)):

                    result = message["result"]

                    if "data" in result and result.get("channel") == "book":
                        subscription = result.get("subscription")

                        test_logger.info("=" * 80)
                        test_logger.info(f"✅ 收到订单簿数据推送")
                        test_logger.info(f"订阅: {subscription}")
                        test_logger.info("=" * 80)
                        # 验证是否是我们订阅的频道
                        if subscription == channel:
                            book_data = message
                            break
                        else:
                            test_logger.warning(f"⚠️ 收到其他频道的数据: {subscription}")
                            continue

                    test_logger.info(f"📬 收到其他消息，继续等待...")

                    # 检查是否收到数据
                    if book_data is None:
                        error_msg = f"❌ 未能在 {max_attempts} 次尝试中收到订单簿数据推送"
                        test_logger.error(error_msg)
                        raise AssertionError(error_msg)

                    # 保存订单簿数据
                    if save_response:
                        save_response(
                            case_id=case_id,
                            step="orderbook_data",
                            data=book_data
                        )

                    # 添加到 Allure 报告
                    allure.attach(
                        json.dumps(book_data, indent=2, ensure_ascii=False),
                        name="2. 订单簿数据推送",
                        attachment_type=allure.attachment_type.JSON
                    )

                with allure.step("4. 验证订单簿数据推送消息结构"):
                    result = book_data["result"]

                    # 验证推送消息结构
                    validator.validate_book_push_message(
                        book_data,
                        expected_subscription=channel,
                        expected_depth=depth
                    )
                    test_logger.info("✅ 推送消息结构验证通过")

                with allure.step("5. 输出订单簿详细信息"):
                    if len(result["data"]) > 0:
                        snapshot = result["data"][0]
                        bids = snapshot.get("bids", [])
                        asks = snapshot.get("asks", [])
                        timestamp = snapshot.get("t")

                        test_logger.info("=" * 80)
                        test_logger.info("📸 订单簿快照详情:")
                        test_logger.info(f"  时间戳: {timestamp}")
                        test_logger.info(f"  买单数量: {len(bids)}")
                        test_logger.info(f"  卖单数量: {len(asks)}")
                        test_logger.info("=" * 80)

                        # 显示前3档买卖盘
                        test_logger.info("📈 买盘（Bids）前3档:")
                        for i, bid in enumerate(bids[:3]):
                            test_logger.info(f"  {i + 1}. 价格: {bid[0]}, 数量: {bid[1]}, 订单数: {bid[2]}")

                        test_logger.info("📉 卖盘（Asks）前3档:")
                        for i, ask in enumerate(asks[:3]):
                            test_logger.info(f"  {i + 1}. 价格: {ask[0]}, 数量: {ask[1]}, 订单数: {ask[2]}")

                test_logger.info("=" * 80)
                test_logger.info(f"🎉 测试用例 {case_id} 执行完成")
                test_logger.info("=" * 80)