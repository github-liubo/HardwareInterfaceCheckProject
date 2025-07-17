import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import wmi

PASSWORD = "0605xz"  # 默认密码，可修改
EXPIRY_DATE = datetime(2025, 8, 31)  # 密码有效期截止日
CHECK_INTERVAL = 3000  # 检测间隔时间（毫秒），3000=3秒


def center_window(window, width, height):
    """通用窗口居中函数：将窗口定位到屏幕正中央"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


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


def show_password_window():
    """显示密码输入窗口（居中显示）"""
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

    password_window.bind("<Return>", lambda event: verify_password())
    password_window.mainloop()


def show_progress_message():
    """显示持续检测窗口（居中显示）"""
    global app_window, status_label

    app_window = tk.Tk()
    app_window.title("系统提示")
    center_window(app_window, 400, 300)

    status_label = tk.Label(
        app_window,
        text="正在启动检测，请勿操作...",
        font=("微软雅黑", 14),
        wraplength=350,
        justify="center"
    )
    status_label.pack(expand=True)

    # 启动第一次检测
    app_window.after(500, detect_hardware)
    app_window.mainloop()


# -------------------------- 状态提示函数修改 --------------------------
def update_status(text, fg_color="black"):
    """统一更新状态文本的函数"""
    if status_label and app_window:
        status_label.config(text=text, fg=fg_color)


def show_password_keyboard_message():
    return "密码键盘正确接入 状态：OK"


def show_card_reader_message():
    return "读卡器正确接入 状态：OK"


def show_adapter_message():
    return "转接器正确接入 状态：OK"


def show_password_keyboard_error():
    return "密码键盘未正确接入 状态：异常"


def show_card_reader_error():
    return "读卡器未正确接入 状态：异常"


def show_adapter_error():
    return "转接器未正确接入 状态：异常"


# -------------------------- 循环检测函数 --------------------------
def get_windows_usb_devices():
    c = wmi.WMI()
    usb_devices = []
    for usb_controller in c.Win32_USBController():
        for usb_device in usb_controller.associators(wmi_result_class="Win32_PnPEntity"):
            usb_devices.append({
                "name": usb_device.Name,
                "status": usb_device.Status,
                "device_id": usb_device.DeviceID
            })
    return usb_devices


def detect_hardware():
    # 定义需要检测的设备模式
    patterns = [
        [("USB 输入设备", "OK"), ("HID Keyboard Device", "OK")],  # 密码键盘
        [("USB 输入设备", "OK"), ("HID-compliant mouse", "OK")],  # 读卡器
        [("USB 输入设备", "OK"), ("符合 HID 标准的条形码标记读取器", "OK")]  # 转接器
    ]

    # 模式匹配成功时的回调（返回状态文本）
    callbacks = [
        show_password_keyboard_message,  # 密码键盘正常
        show_card_reader_message,        # 读卡器正常
        show_adapter_message             # 转接器正常
    ]

    # 每次检测前重置状态
    pattern_matched = [False] * len(patterns)
    pattern_progress = [0] * len(patterns)
    status_texts = []

    # 遍历设备检测模式
    for device in get_windows_usb_devices():
        for i, pattern in enumerate(patterns):
            current_step = pattern_progress[i]
            if current_step >= len(pattern):
                continue
            expected_name, expected_status = pattern[current_step]
            if device['name'] == expected_name and device['status'] == expected_status:
                pattern_progress[i] += 1
                if pattern_progress[i] == len(pattern):
                    status_texts.append(callbacks[i]())
                    pattern_matched[i] = True
                    pattern_progress[i] = 0
            else:
                pattern_progress[i] = 0

    # 检查未匹配的模式（异常状态）
    if not pattern_matched[0]:
        status_texts.append(show_password_keyboard_error())
    if not pattern_matched[1]:
        status_texts.append(show_card_reader_error())
    if not pattern_matched[2]:
        status_texts.append(show_adapter_error())

    # 更新状态显示
    if status_texts:
        update_status("\n\n".join(status_texts))
    else:
        update_status("未检测到任何设备", "orange")

    # 设定下次检测时间（循环调用）
    app_window.after(CHECK_INTERVAL, detect_hardware)


if __name__ == "__main__":
    show_password_window()