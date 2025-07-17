import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import wmi

PASSWORD = "0605xz"  # 默认密码，可修改
EXPIRY_DATE = datetime(2025, 8, 31)  # 密码有效期截止日


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
    """显示恢复进度窗口（居中显示）"""
    global app_window, status_label

    app_window = tk.Tk()
    app_window.title("系统提示")
    center_window(app_window, 400, 300)

    status_label = tk.Label(
        app_window,
        text="正在检测，请先不要操作",
        font=("微软雅黑", 14),
        wraplength=350,
        justify="center"
    )
    status_label.pack(expand=True)

    app_window.after(500, detect_hardware)
    app_window.mainloop()


def show_completion_message():
    global status_label, app_window
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "硬件检测完毕，15秒后关闭窗口"
        else:
            new_text = current_text + "\n\n" + "硬件检测完毕，15秒后关闭窗口"

        status_label.config(text=new_text, fg="#32CD32")
        app_window.after(15000, app_window.destroy)
    else:
        print("窗口未初始化，无法更新状态-检测完毕")


# -------------------------- 正常提示函数 --------------------------
def show_password_keyboard_message():
    """密码键盘正常接入提示"""
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "密码键盘正确接入 状态：OK"
        else:
            new_text = current_text + "\n\n" + "密码键盘正确接入 状态：OK"
        status_label.config(text=new_text, fg="#32CD32")
        print("密码键盘已接入")
    else:
        print("窗口未初始化，无法更新状态-密码键盘正常")


def show_card_reader_message():
    """读卡器正常接入提示"""
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "读卡器正确接入 状态：OK"
        else:
            new_text = current_text + "\n\n" + "读卡器正确接入 状态：OK"
        status_label.config(text=new_text, fg="#32CD32")
        print("读卡器已接入")
    else:
        print("窗口未初始化，无法更新状态-读卡器正常")

def show_adapter_message():
    """转接器正常接入提示"""
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "转接正确接入 状态：OK"
        else:
            new_text = current_text + "\n\n" + "转接器正确接入 状态：OK"
        status_label.config(text=new_text, fg="#32CD32")
        print("转接器已接入")
    else:
        print("窗口未初始化，无法更新状态-转接器正常")
# -------------------------- 异常提示函数 --------------------------
def show_password_keyboard_error():
    """密码键盘未接入异常提示"""
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "密码键盘未正确接入 状态：异常"
        else:
            new_text = current_text + "\n\n" + "密码键盘未正确接入 状态：异常"
        status_label.config(text=new_text, fg="red")  # 红色字体标记异常
        print("密码键盘未正确接入")
    else:
        print("窗口未初始化，无法更新状态-密码键盘异常")


def show_card_reader_error():
    """读卡器未接入异常提示"""
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "读卡器未正确接入 状态：异常"
        else:
            new_text = current_text + "\n\n" + "读卡器未正确接入 状态：异常"
        status_label.config(text=new_text, fg="red")  # 红色字体标记异常
        print("读卡器未正确接入")
    else:
        print("窗口未初始化，无法更新状态-读卡器异常")

def show_adapter_error():
    """转接器未接入异常提示"""
    if status_label and app_window:
        current_text = status_label.cget("text")
        if current_text == "正在检测，请先不要操作":
            new_text = "转接器未正确接入 状态：异常"
        else:
            new_text = current_text + "\n\n" + "转接器未正确接入 状态：异常"
        status_label.config(text=new_text, fg="red")  # 红色字体标记异常
        print("转接器未正确接入")
    else:
        print("窗口未初始化，无法更新状态-读卡器异常")
# -------------------------- 扫描设备函数 --------------------------
def get_windows_usb_devices():
    c = wmi.WMI()
    usb_devices = []
    for usb_controller in c.Win32_USBController():
        for usb_device in usb_controller.associators(wmi_result_class="Win32_PnPEntity"):
            if usb_device.Status == "OK":
                usb_devices.append({
                    "name": usb_device.Name,
                    "status": usb_device.Status,
                    "device_id": usb_device.DeviceID
                })
    return usb_devices


def detect_hardware():
    # 定义需要检测的设备模式（与需求对应）
    patterns = [
        [("USB 输入设备", "OK"), ("HID Keyboard Device", "OK")],  # 模式0：密码键盘
        [("USB 输入设备", "OK"), ("HID-compliant mouse", "OK")],  # 模式1：读卡器（按需求对应）
        [("USB 输入设备", "OK"), ("符合 HID 标准的条形码标记读取器", "OK")]
    ]

    # 模式匹配成功时的回调（正常提示）
    callbacks = [
        show_password_keyboard_message,  # 模式0匹配成功：密码键盘正常
        show_card_reader_message,        # 模式1匹配成功：读卡器正常
        show_adapter_message             # 模式2匹配成功：转接器正常
    ]

    # 记录每个模式是否匹配成功（初始为False）
    pattern_matched = [False] * len(patterns)
    pattern_progress = [0] * len(patterns)

    # 遍历设备检测模式
    for device in get_windows_usb_devices():
        print(f"检查设备: name={device['name']}, status={device['status']}")
        for i, pattern in enumerate(patterns):
            current_step = pattern_progress[i]
            if current_step >= len(pattern):
                continue
            expected_name, expected_status = pattern[current_step]
            if device['name'] == expected_name and device['status'] == expected_status:
                pattern_progress[i] += 1
                if pattern_progress[i] == len(pattern):
                    callbacks[i]()  # 触发正常提示
                    pattern_matched[i] = True  # 标记为匹配成功
                    pattern_progress[i] = 0
            else:
                pattern_progress[i] = 0

    # 检测结束后：未匹配的模式触发异常提示
    if not pattern_matched[0]:  # 模式0未匹配（密码键盘）
        show_password_keyboard_error()
    if not pattern_matched[1]:  # 模式1未匹配（读卡器）
        show_card_reader_error()
    if not pattern_matched[2]:  # 模式2未匹配（转接器）
        show_adapter_error()

    # 最后显示检测完成
    show_completion_message()


if __name__ == "__main__":
    show_password_window()