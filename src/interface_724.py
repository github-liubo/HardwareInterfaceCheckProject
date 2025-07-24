import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import wmi
import re
import pystray
from PIL import Image, ImageDraw

# 配置项
PASSWORD = "0605xz"
EXPIRY_DATE = datetime(2025, 8, 31)
VERSION = "v1.1"

# 全局变量
root = None
password_window = None
app_window = None
status_frame = None
labels = []
result_count = 0
error_count = 0


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
    password_window = tk.Toplevel(root)
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

    tk.Label(
        password_window,
        text=VERSION,
        font=("微软雅黑", 8),
        fg="gray"
    ).place(x=285, y=120, anchor="ne")

    password_window.bind("<Return>", lambda event: verify_password())


# 显示检测进度窗口
def show_progress_message():
    global app_window, status_frame, labels, result_count, error_count
    labels = []
    result_count = 0
    error_count = 0  # 重置异常计数

    app_window = tk.Toplevel(root)
    app_window.title("系统提示")
    center_window(app_window, 500, 350)

    status_frame = tk.Frame(app_window)
    status_frame.pack(expand=True, padx=20, pady=20)

    initial_label = tk.Label(
        status_frame,
        text="正在检测，请先不要操作",
        font=("微软雅黑", 18)
    )
    initial_label.grid(row=0, column=0, columnspan=2, pady=10)
    labels.append(initial_label)

    # 修改窗口关闭行为：隐藏而不是退出
    def on_close():
        app_window.withdraw()

    app_window.protocol("WM_DELETE_WINDOW", on_close)

    app_window.after(500, detect_hardware)


# 根据错误数量显示不同的完成信息
def show_completion_message():
    global status_frame, labels, result_count, error_count
    if status_frame and app_window:
        if error_count == 0:
            message = "硬件设备检测正常"
            color = "#32CD32"  # 绿色
        else:
            message = f"请检查异常的设备"
            color = "red"  # 红色

        # 打印检测结果汇总
        print(f"\n===== 检测完成 =====")
        print(f"总异常设备数: {error_count}")
        print(f"最终状态: {message}\n")

        completion_label = tk.Label(
            status_frame,
            text=message,
            font=("微软雅黑", 18),
            fg=color
        )
        row = (result_count // 2) + 1
        completion_label.grid(row=row, column=0, columnspan=2, pady=20)
        labels.append(completion_label)
    else:
        print("窗口未初始化，无法更新状态-检测完毕")


# 正常提示函数（添加打印）
def show_password_keyboard_message():
    status = "密码键盘：OK"
    print(f"检测状态: {status}")  # 打印正常状态
    update_status(status, "#32CD32")


def show_card_reader_message():
    status = "读卡器：OK"
    print(f"检测状态: {status}")
    update_status(status, "#32CD32")


def show_adapter_message():
    status = "转接器：OK"
    print(f"检测状态: {status}")
    update_status(status, "#32CD32")


def show_medicare_code_message():
    status = "医保码：OK"
    print(f"检测状态: {status}")
    update_status(status, "#32CD32")


def show_mouse_message():
    status = "鼠标：OK"
    print(f"检测状态: {status}")
    update_status(status, "#32CD32")


# 异常提示函数（添加打印）
def show_password_keyboard_error():
    global error_count
    error_count += 1
    status = "密码键盘：异常"
    print(f"检测状态: {status}")  # 打印异常状态
    update_status(status, "red")


def show_card_reader_error():
    global error_count
    error_count += 1
    status = "读卡器：异常"
    print(f"检测状态: {status}")
    update_status(status, "red")


def show_adapter_error():
    global error_count
    error_count += 1
    status = "转接器：异常"
    print(f"检测状态: {status}")
    update_status(status, "red")


def show_medicare_code_error():
    global error_count
    error_count += 1
    status = "医保码：异常"
    print(f"检测状态: {status}")
    update_status(status, "red")


def show_mouse_error():
    global error_count
    error_count += 1
    status = "鼠标：异常"
    print(f"检测状态: {status}")
    update_status(status, "red")


# 通用状态更新函数
def update_status(message, color):
    global status_frame, labels, result_count, app_window
    if status_frame and app_window:
        if result_count == 0 and labels:
            initial_label = labels[0]
            initial_label.grid_remove()

        result_count += 1

        new_label = tk.Label(
            status_frame,
            text=message,
            font=("微软雅黑", 18),
            fg=color
        )

        row = (result_count - 1) // 2 + 1
        col = (result_count - 1) % 2

        new_label.grid(row=row, column=col, padx=30, pady=20, sticky="w")
        labels.append(new_label)


# 硬件检测逻辑（核心：添加设备信息打印）
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

    print("===== 找到的设备列表（含 VID/PID） =====")
    print(f"{'名称':<30} | 状态 | {'VID/PID':<15} | 设备ID")

    for dev in devices:
        vid_pid = dev['vid_pid']
        if vid_pid:
            print(f"{dev['name']:<30} | {dev['status']}  | {vid_pid:<15} | {dev['device_id']}")
    device_patterns = [
        {
            "name": "密码键盘",
            "devices": [("USB 输入设备", "OK"), ("符合 HID 标准的条形码标记读取器", "OK")],
            "callback_ok": show_password_keyboard_message,
            "callback_err": show_password_keyboard_error,
        },
        {
            "name": "读卡器",
            "devices": [("USB 输入设备", "OK"), ("符合 HID 标准的供应商定义设备", "OK")],
            "callback_ok": show_card_reader_message,
            "callback_err": show_card_reader_error,
        },
        {
            "name": "医保码",
            "devices": [("USB 输入设备", "OK"), ("HID Keyboard Device", "OK")],
            "callback_ok": show_medicare_code_message,
            "callback_err": show_medicare_code_error,
        },
        {
            "name": "鼠标",
            "devices": [("USB 输入设备", "OK"), ("HID-compliant mouse", "OK")],
            "callback_ok": show_mouse_message,
            "callback_err": show_mouse_error,
        }
    ]

    print("\n===== 开始检测设备 =====")
    for pattern_info in device_patterns:
        pattern_name = pattern_info["name"]
        pattern_devices = pattern_info["devices"]
        callback_ok = pattern_info["callback_ok"]
        callback_err = pattern_info["callback_err"]

        print(f"\n检测 {pattern_name}...")
        matched_devices = []
        for expected_name, expected_status in pattern_devices:
            print(f"  查找设备: 名称={expected_name}, 状态={expected_status}")
            for dev in devices:
                if dev["name"] == expected_name and dev["status"] == expected_status:
                    matched_devices.append(dev)
                    print(f"  找到匹配设备: {dev['name']} (状态: {dev['status']})")
                    break
            else:
                print(f"  未找到匹配设备: {expected_name} (状态: {expected_status})")

        if len(matched_devices) == len(pattern_devices) and len(set(dev["vid_pid"] for dev in matched_devices)) == 1:
            callback_ok()
        else:
            callback_err()

    show_completion_message()


