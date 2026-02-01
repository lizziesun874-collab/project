CryptoAPIAuto - WebSocket & Restful 自动化测试框架
本项目是基于 Pytest + Allure + Asyncio 构建的交易所 API 自动化测试框架，支持高频 WebSocket 订单簿数据校验及 Restful 接口测试。


CryptoAPIAuto/
├── .pytest_cache/            # Pytest 缓存目录
├── allure-results/           # Allure 报告原始数据目录
├── config/                   # 配置相关文件
├── data/                     # 测试数据（如：各个 Case 的 JSON 配置）
│   ├── base_data_loader.py
│   ├── boundary_cases.py     #task1 测试数据
│   ├── combination_cases.py  #task1 测试数据
│   ├── negative_cases.py     #task1 测试数据
│   ├── performance_cases.py  #task1 测试数据
│   ├── positive_cases.py     #task1 测试数据
│   ├── orderbook_cases.py    #task2 测试数据
│   └── ws_data_loader.py
├── reports/                  # 测试报告输出目录
├── tests/                    # 测试用例目录
│   ├── backup/
│   ├── conftest.py           # Pytest 核心配置与 Fixtures
│   └── test_orderbook.py     # 订单簿 WebSocket 测试用例
└── utils/                    # 工具类与辅助函数
    ├── api_client.py         # Restful API 客户端
    ├── helpers.py
    ├── validators.py         # 数据校验器
    └── ws_client.py          # WebSocket 客户端


**🚀 快速开始**
1. 安装依赖
bash
pip install -r requirements.txt
pip install pytest-rerunfailures  # 新增：用于支持重试机制
2. 执行测试命令
执行全部用例：pytest tests/ -v
3. 执行单个测试类（使用 Node ID 语法）：
bash
pytest tests/test_orderbook.py::TestOrderbook
4. 疑难问题定位
task2:
   1. websocket 在UAT环境有数据（但是bids和asks没数据），prod环境链接超时
      * 怀疑websockts 版本和Python3.7 版本问题，试过websocket-client 
      * IP是否在某个国家被限制 
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
   2. case 执行过程中卡主，没有正常退出
      * subscribe 有个do while 死循环

**报告与日志**
生成 Allure 报告：执行以下命令启动本地报告服务，并在浏览器中查看。
bash
allure serve ./allure-results
Use code with caution.

响应快照：所有关键步骤的 JSON 响应均自动保存至 reports/responses/。
重试记录：在 Allure 报告的 "Retries" 选项卡中可查看用例的所有重试历史。

   
