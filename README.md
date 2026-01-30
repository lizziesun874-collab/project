V1:test_data.py
V2:test_data_positive.py
实现用caseid获取case，但是测试数据和数据提取放在一个文件，还有各种数据data




V3:
test_data_loader.py
performance_cases.py

task2:
1. websocket 在UAT环境有数据（但是bids和asks没数据），prod环境链接超时
   * websockts 版本和Python3.7 版本问题，试过websocket-client 
   * IP在某个国家被限制 
   * 同一台电脑的postman prod环境可以正常访问（定位出在连接时加代理信息）
     * # 1. 创建代理对象
            proxy = Proxy.from_url("http://127.0.0.1:7890")

            # 2. 手动通过代理连接到目标主机的 443 端口
            # stream.crypto.com 这里的域名要和 ws_url 的主机名一致
            sock = await proxy.connect(dest_host="stream.crypto.com", dest_port=443,
                timeout=self.timeout)

            self.ws = await asyncio.wait_for(
                websockets.connect(
                    self.ws_url,
                    sock=sock,  # 关键点：直接使用代理握手后的 socket
                    server_hostname="stream.crypto.com",
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10,
                ),
* case 执行过程中卡主，没有正常退出
  * subscribe 有个do while 死循环
*  Allure
  * pytest --alluredir=reports/allure-results
  * allure serve ./reports/allure-results

   
