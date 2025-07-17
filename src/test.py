# import pyudev
# import time
#
# context = pyudev.Context()
# monitor = pyudev.Monitor.from_netlink(context)
# monitor.filter_by(subsystem='usb')
#
# # 异步监控
# observer = pyudev.MonitorObserver(
#     monitor,
#     callback=lambda device: print(f"设备变化: {device.action} - {device.get('PRODUCT')}"),
#     name='usb-monitor'
# )
# observer.start()
#
# # 保持主线程运行
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()