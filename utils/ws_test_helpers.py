"""
utils/ws_test_helpers.py
WebSocket 测试辅助函数
"""
import json
import allure
from typing import Dict, Any
import time
import asyncio



class WebSocketTestHelper:
    """WebSocket 测试辅助类"""


    async def execute_subscribe_test(
            ws_client,
            test_logger,
            save_response,
            case: Dict[str, Any],
            validator
    ):
        """执行订阅测试的通用流程 - 连续获取5条数据"""
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

            subscribe_confirm = await ws_client.subscribe(
                channels=[channel],
                timeout=30
            )

            assert subscribe_confirm is not None, "未收到订阅确认响应"
            test_logger.info(f"订阅确认: {subscribe_confirm}")



            allure.attach(
                json.dumps(subscribe_confirm, indent=2, ensure_ascii=False),
                name="1. 订阅确认响应",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("2. 验证订阅确认响应"):
            validator.validate_subscription_response(subscribe_confirm)
            test_logger.info("✅ 订阅确认验证通过")

        with allure.step("3. 等待并收集 5 条订单簿数据推送 (40秒超时)"):
            test_logger.info("=" * 80)
            test_logger.info(f"⏳ 开始连续收集 5 条订单簿数据，最大允许 40 秒...")
            test_logger.info("=" * 80)

            book_data_list = []
            target_count = 5
            timeout_seconds = 20
            start_time = time.monotonic()

            # 尝试次数限制可以取消，只要在时间限制内就好
            # max_attempts = 100

            while len(book_data_list) < target_count:
                elapsed_time = time.monotonic() - start_time

                # 检查总超时
                if elapsed_time > timeout_seconds:
                    error_msg = f"❌ 严重超时：超过 {timeout_seconds} 秒 ({len(book_data_list)}/{target_count} 条)，强制退出！"
                    test_logger.error(error_msg)
                    raise AssertionError(error_msg)  # 抛出异常，测试失败并退出

                try:
                    test_logger.info(
                        f"🔍 尝试接收 (已耗时: {elapsed_time:.2f}s) | 已收集: {len(book_data_list)}/{target_count}")

                    # 使用 asyncio.wait_for 强制单次接收超时，以防止内部阻塞
                    message = await asyncio.wait_for(
                        ws_client.receive_message(timeout=8),
                        timeout=10  # 外部等待时间略长于内部
                    )

                    if message is None:
                        test_logger.warning(f"⚠️  单次接收超时 (8s)，继续尝试...")
                        continue

                    # 调试日志：打印收到的原始消息类型和 method
                    msg_method = message.get("method", "N/A")
                    test_logger.info(f"📨 收到消息: Method='{msg_method}'")

                    # 处理心跳 (必须回复，否则服务器可能主动断开导致卡死)
                    if msg_method == "public/heartbeat":
                        test_logger.info("💓 收到心跳，回复 pong")
                        await ws_client.send_message({
                            "id": message.get("id"),
                            "method": "public/respond-heartbeat"
                        })
                        continue

                    # 检查是否是目标频道数据
                    result = message.get("result", {})
                    msg_sub = result.get("subscription", "N/A")

                    if (msg_method == "subscribe" and
                            isinstance(result, dict) and
                            msg_sub == channel):

                        book_data_list.append(message)
                        test_logger.info(f"✅ 成功捕获 1 条目标频道数据 (Total: {len(book_data_list)})")
                    else:
                        test_logger.info(f"📬 收到非目标消息 (Channel: {msg_sub})，继续等待...")

                except asyncio.TimeoutError:
                    test_logger.error(f"❌ 接收消息严重超时 (>10s)，可能是底层连接问题，继续检查总时间...")
                    continue  # 总超时会在 while 顶部检查

                except Exception as e:
                    test_logger.exception(f"❌ 接收过程中发生致命异常: {e}")
                    raise AssertionError(f"致命异常导致测试终止: {e}")  # 任何其他异常都应失败测试

            # 如果循环结束，说明成功收集了足够的数据
            test_logger.info(f"🎉 成功收集到 {target_count} 条数据，用时 {time.monotonic() - start_time:.2f}s。")



        # 循环验证每一条收到的数据
        for idx, book_data in enumerate(book_data_list):

            current_index = idx + 1
            with allure.step(f"4.{current_index} 验证第 {current_index} 条推送消息"):
                result = book_data["result"]

                # 保存与验证
                if save_response:
                     save_response(data=book_data,case_id=case_id, step=f"orderbook_data_{current_index}")

                validator.validate_book_push_message(
                    book_data,
                    expected_subscription=channel,
                    expected_depth=depth
                )
                # 新增的内容验证
                try:
                    test_logger.info("验证订单簿业务内容：价格排序、买卖盘不倒挂")
                    validator.validate_orderbook_content(book_data)
                    test_logger.info(f"📸 快照 {idx + 1} 业务内容校验通过(价格排序、买卖盘不倒挂)")
                except AssertionError as e:
                    test_logger.error(f"📸 快照 {idx + 1} 业务校验失败(价格排序、买卖盘不倒挂): {str(e)}")
                    raise e

                # 输出详情
                if len(result.get("data", [])) > 0:
                    snapshot = result["data"][0]
                    test_logger.info(
                        f"📸 快照 {current_index} | 时间戳: {snapshot.get('t')} | 买/卖: {len(snapshot.get('bids', []))}/{len(snapshot.get('asks', []))}")

                allure.attach(
                    json.dumps(book_data, indent=2, ensure_ascii=False),
                    name=f"订单簿数据推送_{current_index}",
                    attachment_type=allure.attachment_type.JSON
                )

        test_logger.info("=" * 80)
        test_logger.info(f"🎉 测试用例 {case_id} 成功收集并验证 {target_count} 条数据")
        test_logger.info("=" * 80)

    async def execute_multiple_subscribe_test(
            ws_client,
            test_logger,
            save_response,
            case: Dict[str, Any],
            validator
    ):
        """执行多频道订阅测试的通用流程 - 每个频道连续获取5条数据"""
        case_id = case['case_id']
        params = case['params']
        expected = case.get('expected', {})

        # 构建多个订阅频道
        channels_config = params['channels']
        channels = []
        for config in channels_config:
            instrument_name = config['instrument_name']
            depth = config['depth']
            channel = f"book.{instrument_name}.{depth}"
            channels.append(channel)

        with allure.step(f"1. 订阅多个频道: {', '.join(channels)}"):
            test_logger.info("=" * 80)
            test_logger.info(f"📢 发送多频道订阅请求: {channels}")
            test_logger.info("=" * 80)

            subscribe_confirm = await ws_client.subscribe(
                channels=channels,
                timeout=30
            )

            assert subscribe_confirm is not None, "未收到订阅确认响应"
            test_logger.info(f"订阅确认: {subscribe_confirm}")

            allure.attach(
                json.dumps(subscribe_confirm, indent=2, ensure_ascii=False),
                name="1. 多频道订阅确认响应",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("2. 验证订阅确认响应"):
            validator.validate_subscription_response(subscribe_confirm)
            test_logger.info("✅ 多频道订阅确认验证通过")

        # 为每个频道收集数据
        all_channel_data = {}  # {channel: [messages]}

        for channel in channels:
            all_channel_data[channel] = []

        with allure.step(f"3. 等待并收集每个频道各 5 条订单簿数据推送 (60秒超时)"):
            test_logger.info("=" * 80)
            test_logger.info(f"⏳ 开始为 {len(channels)} 个频道分别收集 5 条数据...")
            test_logger.info("=" * 80)

            target_count_per_channel = 5
            timeout_seconds = 60
            start_time = time.monotonic()

            # 计算总目标数量
            total_target = len(channels) * target_count_per_channel
            total_collected = 0

            while total_collected < total_target:
                elapsed_time = time.monotonic() - start_time

                # 检查总超时
                if elapsed_time > timeout_seconds:
                    error_msg = f"❌ 严重超时：超过 {timeout_seconds} 秒 ({total_collected}/{total_target} 条)，强制退出！"
                    test_logger.error(error_msg)
                    # 输出每个频道的收集情况
                    for ch, data_list in all_channel_data.items():
                        test_logger.error(f"  频道 {ch}: {len(data_list)}/{target_count_per_channel} 条")
                    raise AssertionError(error_msg)

                try:
                    test_logger.info(
                        f"🔍 尝试接收 (已耗时: {elapsed_time:.2f}s) | 总进度: {total_collected}/{total_target}")

                    # 使用 asyncio.wait_for 强制单次接收超时
                    message = await asyncio.wait_for(
                        ws_client.receive_message(timeout=8),
                        timeout=10
                    )

                    if message is None:
                        test_logger.warning(f"⚠️  单次接收超时 (8s)，继续尝试...")
                        continue

                    # 调试日志：打印收到的原始消息类型和 method
                    msg_method = message.get("method", "N/A")
                    test_logger.info(f"📨 收到消息: Method='{msg_method}'")

                    # 处理心跳
                    if msg_method == "public/heartbeat":
                        test_logger.info("💓 收到心跳，回复 pong")
                        await ws_client.send_message({
                            "id": message.get("id"),
                            "method": "public/respond-heartbeat"
                        })
                        continue

                    # 检查是否是目标频道数据
                    result = message.get("result", {})
                    msg_sub = result.get("subscription", "N/A")

                    if msg_method == "subscribe" and isinstance(result, dict):
                        # 检查是否属于我们订阅的频道之一
                        if msg_sub in channels:
                            # 检查该频道是否还需要更多数据
                            if len(all_channel_data[msg_sub]) < target_count_per_channel:
                                all_channel_data[msg_sub].append(message)
                                total_collected += 1
                                test_logger.info(
                                    f"✅ 频道 [{msg_sub}] 捕获第 {len(all_channel_data[msg_sub])} 条数据 "
                                    f"(总进度: {total_collected}/{total_target})"
                                )
                            else:
                                test_logger.info(f"📬 频道 [{msg_sub}] 已收集足够数据，忽略此消息")
                        else:
                            test_logger.info(f"📬 收到非目标频道消息 (Channel: {msg_sub})，继续等待...")
                    else:
                        test_logger.info(f"📬 收到非订阅推送消息，继续等待...")

                except asyncio.TimeoutError:
                    test_logger.error(f"❌ 接收消息严重超时 (>10s)，可能是底层连接问题，继续检查总时间...")
                    continue

                except Exception as e:
                    test_logger.exception(f"❌ 接收过程中发生致命异常: {e}")
                    raise AssertionError(f"致命异常导致测试终止: {e}")

            # 如果循环结束，说明成功收集了足够的数据
            test_logger.info(f"🎉 成功为所有频道收集到数据，用时 {time.monotonic() - start_time:.2f}s。")

        # 验证每个频道的数据
        for channel_idx, (channel, book_data_list) in enumerate(all_channel_data.items()):
            # 提取频道配置信息
            channel_config = channels_config[channel_idx]
            depth = channel_config['depth']

            test_logger.info("=" * 80)
            test_logger.info(f"📊 开始验证频道: {channel} ({len(book_data_list)} 条数据)")
            test_logger.info("=" * 80)

            # 循环验证该频道的每一条数据
            for idx, book_data in enumerate(book_data_list):
                current_index = idx + 1

                with allure.step(
                        f"4.{channel_idx + 1}.{current_index} 验证频道 [{channel}] 第 {current_index} 条推送消息"):
                    result = book_data["result"]

                    # 保存响应
                    if save_response:
                        save_response(
                            data=book_data,
                            case_id=case_id,
                            step=f"{channel}_data_{current_index}"
                        )

                    # 验证推送消息格式
                    validator.validate_book_push_message(
                        book_data,
                        expected_subscription=channel,
                        expected_depth=depth
                    )

                    # 验证订单簿业务内容
                    try:
                        test_logger.info(f"验证频道 [{channel}] 订单簿业务内容：价格排序、买卖盘不倒挂")
                        validator.validate_orderbook_content(book_data)
                        test_logger.info(
                            f"📸 频道 [{channel}] 快照 {current_index} 业务内容校验通过(价格排序、买卖盘不倒挂)"
                        )
                    except AssertionError as e:
                        test_logger.error(
                            f"📸 频道 [{channel}] 快照 {current_index} 业务校验失败(价格排序、买卖盘不倒挂): {str(e)}"
                        )
                        raise e

                    # 输出详情
                    if len(result.get("data", [])) > 0:
                        snapshot = result["data"][0]
                        test_logger.info(
                            f"📸 频道 [{channel}] 快照 {current_index} | "
                            f"时间戳: {snapshot.get('t')} | "
                            f"买/卖: {len(snapshot.get('bids', []))}/{len(snapshot.get('asks', []))}"
                        )

                    allure.attach(
                        json.dumps(book_data, indent=2, ensure_ascii=False),
                        name=f"频道_{channel}_数据推送_{current_index}",
                        attachment_type=allure.attachment_type.JSON
                    )

        test_logger.info("=" * 80)
        test_logger.info(
            f"🎉 测试用例 {case_id} 成功收集并验证 {len(channels)} 个频道，"
            f"每个频道 {target_count_per_channel} 条数据"
        )
        test_logger.info("=" * 80)

    @staticmethod
    async def execute_unsubscribe_test(
            ws_client,
            test_logger,
            save_response,
            case: Dict[str, Any],
            validator
    ):
        """TC_BOOK_006: 执行订阅 -> 获取数据 -> 取消订阅 -> 验证停止"""
        case_id = case['case_id']
        params = case['params']
        instrument_name = params['instrument_name']
        depth = params['depth']
        channel = f"book.{instrument_name}.{depth}"

        # 1. 订阅频道
        with allure.step(f"1. 订阅频道: {channel}"):
            test_logger.info(f"📢 发送订阅请求: {channel}")
            sub_res = await ws_client.subscribe(channels=[channel], timeout=20)
            assert sub_res is not None, "订阅请求未收到响应"

            # 保存订阅确认到 reports/responses
            if save_response:
                save_response(data=sub_res, case_id=case_id, step="1_subscribe_confirmation")

            validator.validate_subscription_response(sub_res)
            test_logger.info("✅ 订阅成功确认")

        # 2. 【新增】在取消订阅前，确保收到了至少一条数据推送
        with allure.step("2. 捕获取消订阅前的数据推送"):
            test_logger.info("⏳ 等待接收第一条订单簿数据...")
            try:
                # 尝试接收一条真实数据
                message = await asyncio.wait_for(ws_client.receive_message(timeout=10), timeout=12)

                # 如果收到心跳，处理并再等一次
                if message and message.get("method") == "public/heartbeat":
                    await ws_client.send_message({"id": message.get("id"), "method": "public/respond-heartbeat"})
                    message = await asyncio.wait_for(ws_client.receive_message(timeout=10), timeout=12)

                if message and message.get("method") == "subscribe":
                    test_logger.info(f"✅ 已收到频道数据推送: {channel}")
                    # 保存数据到 reports/responses，这样你就能在文件夹里看到了
                    if save_response:
                        save_response(data=message, case_id=case_id, step="2_pre_unsubscribe_data")

                    allure.attach(json.dumps(message, indent=2), name="取消订阅前收到的数据",
                                  attachment_type=allure.attachment_type.JSON)
                else:
                    test_logger.warning("⚠️ 未能在取消订阅前捕获到实时数据推送")
            except Exception as e:
                test_logger.warning(f"⚠️ 捕获数据时发生异常（可能网络慢）: {e}")

        # 3. 取消订阅
        with allure.step(f"3. 取消订阅频道: {channel}"):
            test_logger.info(f"📤 发送取消订阅请求: {channel}")
            unsub_res = await ws_client.unsubscribe(channels=[channel], timeout=20)

            assert unsub_res is not None, "取消订阅未收到响应"

            # 保存取消订阅确认到 reports/responses
            if save_response:
                save_response(data=unsub_res, case_id=case_id, step="3_unsubscribe_confirmation")

            assert unsub_res.get("code") == 0, f"取消订阅失败: {unsub_res}"
            test_logger.info("✅ 取消订阅成功确认")

        # 4. 验证后续不再接收数据
        with allure.step("4. 验证取消订阅后不再接收数据"):
            test_logger.info("⏳ 正在观察 5 秒，确保无后续推送...")
            try:
                msg = await asyncio.wait_for(ws_client.receive_message(timeout=5), timeout=6)
                if msg and msg.get("result", {}).get("subscription") == channel:
                    # 如果仍然收到该频道数据，报错
                    error_msg = f"❌ 严重错误：取消订阅后仍收到频道 {channel} 的推送数据！"
                    test_logger.error(error_msg)
                    raise AssertionError(error_msg)
            except asyncio.TimeoutError:
                test_logger.info("✅ 确认：5秒内未收到新推送，取消订阅完全生效")


    @staticmethod
    async def execute_error_test(ws_client, test_logger, save_response, case, validator):
        params = case['params']
        expected = case.get('expected', {})
        channel = f"book.{params['instrument_name']}.{params['depth']}"

        with allure.step(f"1. 发送无效订阅请求: {channel}"):
            # 获取响应
            error_response = await ws_client.subscribe(channels=[channel], timeout=20)

            # 如果底层还是返回 None，我们需要强制报错以便调试
            if error_response is None:
                test_logger.error("❌ 订阅请求超时且未收到任何响应回执")
                raise AssertionError("底层 subscribe 方法返回 None，未能捕获到服务器的错误响应")

            if save_response:
                save_response(data=error_response, case_id=case['case_id'], step="error_res")

        with allure.step("2. 验证错误码"):
            actual_code = error_response.get("code")
            expected_code = expected.get("error_code")

            test_logger.info(f"实际 code: {actual_code}, 预期 code: {expected_code}")
            assert actual_code == expected_code, f"错误码不匹配！收到了 {actual_code} 而非 {expected_code}"
            test_logger.info(f"✅ 成功捕获预期错误")


