import websocket
import ssl

# 定义代理信息（来自你的 curl 日志）
proxy_host = "127.0.0.1"
proxy_port = 7890

def on_message(ws, message):
    print(f"收到数据: {message}")

def on_error(ws, error):
    print(f"报错: {error}")

# 选择你要连接的端点
url = "wss://stream.crypto.com/exchange/v1/market"

ws = websocket.WebSocketApp(
    url,
    on_message=on_message,
    on_error=on_error
)

# 关键：显式传入代理参数，并跳过证书校验（防止 Anaconda 证书路径问题）
ws.run_forever(
    http_proxy_host=proxy_host,
    http_proxy_port=proxy_port,
    proxy_type="http",
    sslopt={"cert_reqs": ssl.CERT_NONE}
)
