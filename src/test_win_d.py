import wmi
import time
import logging

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='usb_monitor.log',  # 日志文件名
    filemode='a'  # 追加模式
)

# 添加控制台输出（可选）
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def get_usb_devices():
    c = wmi.WMI()
    usb_devices = []

    # 查询Win32_USBControllerDevice关联类获取USB设备
    for usb_controller in c.Win32_USBController():
        for device in usb_controller.associators(wmi_result_class="Win32_PnPEntity"):
            if device.Status == "OK":  # 只获取状态正常的设备
                usb_devices.append({
                    "name": device.Name,
                    "description": device.Description,
                    "device_id": device.DeviceID
                })
    return usb_devices

# 持续监控USB设备变化
# if __name__ == "__main__":
#     logging.info("===== USB设备监控程序启动 =====")
#     known_devices = set()
#
#     while True:
#         current_devices = set()
#         for device in get_usb_devices():
#             device_id = device["device_id"]
#             current_devices.add(device_id)
#
#             if device_id not in known_devices:
#                 logging.info(f"新设备插入: {device['name']}")
#                 logging.info(f"描述: {device['description']}")
#                 logging.info(f"设备ID: {device_id}")
#                 logging.info("-" * 30)
#
#         # 检查已移除的设备
#         for device_id in known_devices - current_devices:
#             logging.info(f"设备已移除: {device_id}")
#
#         known_devices = current_devices
#         time.sleep(1)  # 每秒检查一次