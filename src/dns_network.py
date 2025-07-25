import socket

def check_network_dns(host="www.baidu.com", timeout=5):
    """
    通过DNS解析检测网络
    :param host: 目标域名
    :param timeout: 超时时间（秒）
    :return: True（解析成功）/False（解析失败）
    """
    try:
        # 解析域名获取IP
        socket.gethostbyname_ex(host)
        return True
    except socket.timeout:
        return False
    except:
        return False

# 测试
# if check_network_dns():
#     print("DNS解析正常")
# else:
#     print("DNS解析失败")