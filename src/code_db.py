import tkinter as tk
from tkinter import ttk
import wmi
import threading
import time


class USBDeviceDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("USB设备检测")
        self.root.geometry("300x200")

        # 创建状态标签
        self.status_label = ttk.Label(
            root,
            text="等待设备连接...",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=50)

        # 创建刷新按钮
        self.refresh_button = ttk.Button(
            root,
            text="刷新状态",
            command=self.check_devices
        )
        self.refresh_button.pack(pady=20)

        # 启动后台检测线程
        self.stop_event = threading.Event()
        self.detection_thread = threading.Thread(target=self.background_detection)
        self.detection_thread.daemon = True
        self.detection_thread.start()

        # 确保窗口关闭时线程停止
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_usb_devices(self):
        """获取所有USB设备信息"""
        c = wmi.WMI()
        usb_devices = []

        for device in c.Win32_PnPEntity():
            if device.Status == "OK" and "USB" in device.PNPDeviceID:
                device_info = {
                    "name": device.Name,
                    "device_id": device.PNPDeviceID,
                    "status": device.Status
                }
                usb_devices.append(device_info)
        return usb_devices

    def extract_id_part(self, device_id):
        """从设备ID中提取两个反斜杠之间的部分"""
        parts = device_id.split("\\")
        if len(parts) >= 3:
            return parts[1]
        return None

    def check_card_reader(self):
        """检查读卡器设备状态"""
        usb_devices = self.get_usb_devices()

        # 用于存储匹配的设备
        usb_input_device = None
        hid_device = None

        for device in usb_devices:
            if "USB 输入设备" in device["name"]:
                usb_input_device = device
            elif "符合 HID 标准的供应商定义设备" in device["name"]:
                hid_device = device

        # 检查两个设备是否都存在且ID部分匹配
        if usb_input_device and hid_device:
            id_part1 = self.extract_id_part(usb_input_device["device_id"])
            id_part2 = self.extract_id_part(hid_device["device_id"])

            if id_part1 and id_part2 and id_part1 == id_part2:
                return True

        return False

    def check_devices(self):
        """检查设备并更新状态标签"""
        if self.check_card_reader():
            self.status_label.config(
                text="读卡器：OK",
                foreground="green"
            )
        else:
            self.status_label.config(
                text="读卡器：异常",
                foreground="red"
            )

    def background_detection(self):
        """后台持续检测设备状态"""
        while not self.stop_event.is_set():
            self.check_devices()
            time.sleep(1)  # 每秒检测一次

    def on_closing(self):
        """窗口关闭时的处理"""
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = USBDeviceDetector(root)
    root.mainloop()