# usb_monitor.py

import pythoncom
import wmi
import threading
import time
from datetime import datetime


class USBDetector:
    def __init__(self, callback):
        self.callback = callback
        self._last_event_time = 0
        self._debounce_time = 1  # 防抖时间，单位秒

    def start(self):
        thread = threading.Thread(target=self.listen_usb_events, daemon=True)
        thread.start()

    def listen_usb_events(self):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        watcher = c.Win32_DeviceChangeEvent.watch_for()

        while True:
            try:
                event = watcher()
                self.usb_event_callback(event)
            except Exception as e:
                print("监听USB事件出错:", e)

    def usb_event_callback(self, wmi_event):
        current_time = datetime.now().timestamp()
        if current_time - self._last_event_time < self._debounce_time:  # 防止短时间内多次触发
            return
        self._last_event_time = current_time

        print("检测到设备变化事件：", wmi_event)
        if callable(self.callback):
            self.callback()


def main(callback_function):
    detector = USBDetector(callback=callback_function)
    detector.start()

# if __name__ == "__main__":
#     def test_callback():
#         print("USB 设备状态改变")
#
#     main(test_callback)