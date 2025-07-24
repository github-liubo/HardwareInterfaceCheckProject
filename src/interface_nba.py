import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import wmi
import re

# 配置项
PASSWORD = "0605xz"  # 默认密码，可修改
EXPIRY_DATE = datetime(2025, 8, 31)  # 密码有效期截止日
VERSION = "v1.0"  # 版本号配置

# 全局变量
password_window = None
app_window = None
status_label = None
password_entry = None
result_list = []  # 存储所有检测结果，用于控制显示格式


# 窗口居中函数
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# 验证密码
def verify_password():
    current_date = datetime.now()
    if current_date > EXPIRY_DATE:
        messagebox.showerror("密码过期", "管理员密码已过期，请联系系统管理员！")
        password_entry.delete(0, tk.END)
        return
    password = password_entry.get()
    if password == PASSWORD:
        password_window.destroy()
        show_progress_message()
    else:
        messagebox.showerror("密码错误", "输入的密码不正确，请重试！")
        password_entry.delete(0, tk.END)


# 显示密码输入窗口
def show_password_window():
    global password_window, password_entry

    password_window = tk.Tk()
    password_window.title("身份验证")
    center_window(password_window, 300, 150)
    password_window.resizable(False, False)

    tk.Label(
        password_window,
        text="请输入管理员密码:",
        font=("微软雅黑", 12)
    ).pack(pady=10)

    password_entry = tk.Entry(password_window, show="*", font=("微软雅黑", 12))
    password_entry.pack(pady=10, padx=20, fill=tk.X)
    password_entry.focus_set()

    tk.Button(
        password_window,
        text="确认",
        command=verify_password,
        font=("微软雅黑", 10),
        width=10,
    ).pack(pady=10)

    # 版本信息标签（右下角）
    tk.Label(
        password_window,
        text=VERSION,
        font=("微软雅黑", 8),
        fg="gray"
    ).place(
        x=285,
        y=120,
        anchor="ne"
    )

    password_window.bind("<Return>", lambda event: verify_password())
    password_window.mainloop()


# 显示检测进度窗口
def show_progress_message():
    global app_window, status_label, result_list
    result_list = []  # 每次检测前清空结果列表

    app_window = tk.Tk()
    app_window.title("系统提示")
    center_window(app_window, 500, 350)  # 加宽窗口以容纳一行两个结果

    status_label = tk.Label(
        app_window,
        text="正在检测，请先不要操作",
        font=("微软雅黑", 20),
        justify="center",  # 左对齐，使结果排列更整齐
        wraplength=450  # 放宽换行限制，确保一行能放下两个结果
    )
    status_label.pack(expand=True, padx=5)  # 增加左右边距

    app_window.after(500, detect_hardware)
    app_window.mainloop()


# # 显示检测完成提示
# def show_completion_message():
#     global status_label, app_window, result_list
#     if status_label and app_window:
#         # 将完成提示添加到结果列表
#         result_list.append("硬件检测完毕，15秒后关闭窗口")
#
#         # 按每行两个结果拼接文本
#         line_items = []
#         for i in range(0, len(result_list), 2):
#             line = "  ".join(result_list[i:i + 2])  # 两个结果之间用两个空格分隔
#             line_items.append(line)
#         new_text = "\n".join(line_items)
#
#         status_label.config(text=new_text, fg="#32CD32")
#         app_window.after(15000, app_window.destroy)
#     else:
#         print("窗口未初始化，无法更新状态-检测完毕")


# -------------------------- 提示函数（正常）--------------------------
def show_password_keyboard_message():
    update_status("密码键盘：OK", "#32CD32")


def show_card_reader_message():
    update_status("    读卡器：OK", "#32CD32")


def show_adapter_message():
    update_status("转接器：OK", "#32CD32")


def show_medicare_code_message():
    update_status("医保码：OK", "#32CD32")


def show_mouse_message():
    update_status("    鼠标：OK", "#32CD32")


# -------------------------- 提示函数（异常）--------------------------
def show_password_keyboard_error():
    update_status("密码键盘：异常", "red")


def show_card_reader_error():
    update_status("    读卡器：异常", "red")


def show_adapter_error():
    update_status("转接器：异常", "red")


def show_medicare_code_error():
    update_status("医保码：异常", "red")


def show_mouse_error():
    update_status("    鼠标：异常", "red")


# 通用状态更新函数（核心改进：控制一行显示两个结果）
def update_status(message, color):
    global status_label, app_window, result_list
    if status_label and app_window:
        # 将新结果添加到列表
        result_list.append(message)

        # 按每行两个结果拼接文本
        line_items = []
        for i in range(0, len(result_list), 2):
            line = "  ".join(result_list[i:i + 2])  # 两个结果之间用两个空格分隔
            line_items.append(line)
        new_text = "\n".join(line_items)

        # 更新标签文本，统一使用当前颜色（若需单独颜色需用Text组件，见说明）
        status_label.config(text=new_text, fg=color)
    else:
        print(f"窗口未初始化，无法更新状态 - {message}")


# -------------------------- 硬件检测逻辑 --------------------------
def extract_vid_pid(device_id):
    match = re.search(r"VID_[0-9A-F]{4}&PID_[0-9A-F]{4}", device_id)
    return match.group(0) if match else None


def get_windows_usb_devices():
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
    return devices


def detect_hardware():
    devices = get_windows_usb_devices()

    # 定义需要检测的设备模式
    device_patterns = [
        {
            "name": "密码键盘",
            "devices": [
                ("USB 输入设备", "OK"),
                ("符合 HID 标准的条形码标记读取器", "OK")
            ],
            "callback_ok": show_password_keyboard_message,
            "callback_err": show_password_keyboard_error,
        },
        {
            "name": "读卡器",
            "devices": [
                ("USB 输入设备", "OK"),
                ("符合 HID 标准的供应商定义设备", "OK")
            ],
            "callback_ok": show_card_reader_message,
            "callback_err": show_card_reader_error,
        },
        {
            "name": "医保码",
            "devices": [
                ("USB 输入设备", "OK"),
                ("HID Keyboard Device", "OK")
            ],
            "callback_ok": show_medicare_code_message,
            "callback_err": show_medicare_code_error,
        },
        {
            "name": "鼠标",
            "devices": [
                ("USB 输入设备", "OK"),
                ("HID-compliant mouse", "OK")
            ],
            "callback_ok": show_mouse_message,
            "callback_err": show_mouse_error,
        }
    ]

    # 为每个模式进行设备匹配
    for pattern_info in device_patterns:
        pattern_devices = pattern_info["devices"]
        callback_ok = pattern_info["callback_ok"]
        callback_err = pattern_info["callback_err"]

        matched_devices = []

        for expected_name, expected_status in pattern_devices:
            for dev in devices:
                if dev["name"] == expected_name and dev["status"] == expected_status:
                    matched_devices.append(dev)
                    break  # 找到一个就停止

        if len(matched_devices) == len(pattern_devices):
            vid_pid_set = set(dev["vid_pid"] for dev in matched_devices)
            if len(vid_pid_set) == 1:  # VID/PID 一致
                callback_ok()
            else:
                callback_err()
        else:
            callback_err()

    # 最后显示检测完成
    # show_completion_message()

