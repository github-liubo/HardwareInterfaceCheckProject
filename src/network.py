import subprocess
import time
import re
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    filename='network_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def ping_host(host, count=4):
    """
    执行 ping 命令并解析结果

    返回:
        success_rate: 成功率(%)
        avg_latency: 平均延迟(ms)
    """
    try:
        # 根据操作系统选择合适的 ping 命令
        if subprocess.call(['ping', '-c', '1', '-W', '1', host], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) != 0:
            return 0, float('inf')  # 主机不可达

        # 执行 ping 命令
        result = subprocess.run(
            ['ping', '-c', str(count), '-W', '1', host],
            capture_output=True,
            text=True
        )

        # 解析输出结果
        output = result.stdout

        # 提取丢包率
        match_loss = re.search(r'(\d+)% packet loss', output)
        if not match_loss:
            logging.error(f"无法解析丢包率: {output}")
            return 0, float('inf')
        loss_rate = int(match_loss.group(1))
        success_rate = 100 - loss_rate

        # 提取平均延迟
        match_time = re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms', output)
        if not match_time:
            # 尝试另一种格式
            match_time = re.search(r'round-trip min/avg/max = [\d.]+/([\d.]+)/[\d.]+ ms', output)
        if match_time:
            avg_latency = float(match_time.group(1))
        else:
            logging.warning(f"无法解析延迟: {output}")
            avg_latency = float('inf')

        return success_rate, avg_latency

    except Exception as e:
        logging.error(f"Ping 执行出错: {e}")
        return 0, float('inf')


def monitor_network(host, interval=5, success_threshold=80, latency_threshold=200):
    """
    持续监控网络连接

    参数:
        host: 目标主机IP
        interval: 每次ping之间的间隔(秒)
        success_threshold: 成功率阈值(%)
        latency_threshold: 延迟阈值(ms)
    """
    print(f"开始监控网络连接: {host}")
    print(f"监控参数: 成功率阈值={success_threshold}%, 延迟阈值={latency_threshold}ms, 检查间隔={interval}秒")
    print("-" * 50)

    consecutive_problems = 0

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success_rate, avg_latency = ping_host(host)

            status = "正常"
            problem_reasons = []

            if success_rate < success_threshold:
                status = "异常"
                problem_reasons.append(f"丢包率过高({100 - success_rate}%)")

            if avg_latency > latency_threshold:
                status = "异常"
                problem_reasons.append(f"延迟过高({avg_latency}ms)")

            # 记录日志
            log_msg = f"{timestamp} - 状态: {status} - 成功率: {success_rate}% - 平均延迟: {avg_latency}ms"
            if problem_reasons:
                log_msg += f" - 问题: {', '.join(problem_reasons)}"
                consecutive_problems += 1
                if consecutive_problems >= 3:
                    log_msg += " - 连续多次检测到问题，网络可能存在严重故障!"
                    logging.warning(log_msg)
            else:
                consecutive_problems = 0
                logging.info(log_msg)

            # 打印到控制台
            print(log_msg)

            # 等待下一次检测
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n监控已停止")


# if __name__ == "__main__":
#     TARGET_HOST = "172.16.204.254"  # 目标IP地址
#     CHECK_INTERVAL = 5  # 检查间隔(秒)
#     SUCCESS_THRESHOLD = 80  # 成功率阈值(%)
#     LATENCY_THRESHOLD = 200  # 延迟阈值(ms)
#
#     monitor_network(
#         host=TARGET_HOST,
#         interval=CHECK_INTERVAL,
#         success_threshold=SUCCESS_THRESHOLD,
#         latency_threshold=LATENCY_THRESHOLD
#     )