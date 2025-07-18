import wmi
import re
import tkinter as tk

# 提取 VID&PID
def extract_vid_pid(device_id):
    match = re.search(r"VID_[0-9A-F]{4}&PID_[0-9A-F]{4}", device_id)
    return match.group(0) if match else None

# 检查读卡器状态
def check_reader_status():
    c = wmi.WMI()
    devices = []

    for device in c.Win32_PnPEntity():
        if device.Name and device.DeviceID and device.Status:
            devices.append({
                "name": device.Name,
                "device_id": device.DeviceID,
                "vid_pid": extract_vid_pid(device.DeviceID),
                "status": device.Status
            })

    usb_input = None
    hid_device = None

    for dev in devices:
        if dev["vid_pid"] is None:
            continue
        if "USB 输入设备" in dev["name"] and dev["status"] == "OK":
            usb_input = dev
        elif "符合 HID 标准的供应商定义备" in dev["name"] and dev["status"] == "OK":
            hid_device = dev

    if usb_input and hid_device and usb_input["vid_pid"] == hid_device["vid_pid"]:
        return "读卡器：OK"
    else:
        return "读卡器：异常"

# GUI 显示
def update_label():
    status = check_reader_status()
    label.config(text=status)
    root.after(5000, update_label)  # 每5秒更新一次

# 创建窗口
root = tk.Tk()
root.title("读卡器状态检测")
root.geometry("300x100")

label = tk.Label(root, text="检测中...", font=("Arial", 20))
label.pack(expand=True)

update_label()

root.mainloop()