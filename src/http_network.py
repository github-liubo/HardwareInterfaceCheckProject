import requests

def check_network_http(url="https://www.baidu.com", timeout=5):
    """
    通过HTTP请求检测网络
    :param url: 目标URL（默认百度）
    :param timeout: 超时时间（秒）
    :return: True（网络通畅）/False（网络不通）
    """
    try:
        response = requests.get(url, timeout=timeout)
        # 状态码200-299表示请求成功
        return 200 <= response.status_code < 300
    except:
        return False

# # 测试
# if check_network_http():
#     print("网络通畅")
# else:
#     print("网络不通")