import requests


def check_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_info = response.json()
        print(f"当前 IP: {ip_info['ip']}")

        # 获取 IP 位置信息
        geo = requests.get(f"https://ipapi.co/{ip_info['ip']}/json/", timeout=5)
        print(f"位置信息: {geo.json()}")
    except Exception as e:
        print(f"Error: {e}")


check_ip()