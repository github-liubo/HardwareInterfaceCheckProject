import dns_network
import http_network
import ping_network
def check_network():
    """综合检测网络状态，返回详细结果"""
    ping_ok = ping_network.check_network_ping()
    http_ok = http_network.check_network_http()
    dns_ok = dns_network.check_network_dns()

    result = {
        "网络通畅": ping_ok and http_ok,
        "ping检测": "成功" if ping_ok else "失败",
        "HTTP访问": "成功" if http_ok else "失败",
        "DNS解析": "成功" if dns_ok else "失败"
    }

    if not ping_ok:
        result["原因"] = "底层网络不通（可能网线断开、防火墙拦截）"
    elif not dns_ok:
        result["原因"] = "DNS解析失败（可能DNS服务器异常）"
    elif not http_ok:
        result["原因"] = "HTTP访问失败（可能目标服务器不可达、代理问题）"
    else:
        result["原因"] = "网络正常"

    return result


# 测试
# network_status = check_network()
# print(f"网络状态：{network_status['网络通畅']}")
# print(f"详情：{network_status}")