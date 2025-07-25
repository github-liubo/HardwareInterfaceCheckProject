import os
import platform

def check_network_ping(host="www.baidu.com", count=2):
    """
    通过ping命令检测网络
    :param host: 目标主机（默认百度，国内访问稳定）
    :param count: 发送包的数量
    :return: True（网络通畅）/False（网络不通）
    """
    # 根据系统设置ping参数（-n是Windows，-c是Linux/Mac）
    param = "-n" if platform.system().lower() == "windows" else "-c"
    # 执行ping命令
    command = [f"ping {param} {count} {host}"]
    # 执行命令并获取返回码（0表示成功）
    return os.system(command[0]) == 0

# 测试
# if check_network_ping():
#     print("网络通畅")
# else:
#     print("网络不通")