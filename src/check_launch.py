import json
import os
import tkinter as tk

# 全局变量：最大启动次数和存储文件路径
MAX_LAUNCH_COUNT = 12  # 最大启动次数
COUNT_FILE = "C:\Program Files (x86)\launch_count.json"  # 存储启动次数的文件

def load_launch_count():
    """读取启动次数（从文件加载）"""
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("count", 0)
        except (json.JSONDecodeError, IOError):
            return 0  # 文件损坏时重置为0
    else:
        save_launch_count(0)  # 首次启动创建文件
        return 0

def save_launch_count(count):
    """保存启动次数到文件"""
    try:
        with open(COUNT_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": count}, f, indent=2)
    except IOError as e:
        print(f"保存启动次数失败：{e}")


def check_launch_limit():
    """检查启动次数是否超限"""
    current_count = load_launch_count()
    new_count = current_count + 1  # 本次启动计数+1
    save_launch_count(new_count)  # 立即保存次数

    if new_count > MAX_LAUNCH_COUNT:
        show_limit_window()  # 超限则显示提示窗口
        return False  # 超限
    return True  # 未超限


def show_limit_window():
    """显示使用次数超限窗口"""
    limit_window = tk.Tk()
    limit_window.title("使用限制")
    limit_window.geometry("350x150")
    limit_window.resizable(False, False)

    # 居中显示窗口
    screen_width = limit_window.winfo_screenwidth()
    screen_height = limit_window.winfo_screenheight()
    x = (screen_width // 2) - 175
    y = (screen_height // 2) - 75
    limit_window.geometry(f"+{x}+{y}")

    # 超限提示文本
    tk.Label(
        limit_window,
        text="使用次数超限，请联系管理员重新签注后使用",
        font=("微软雅黑", 12, "bold"),
        fg="red"
    ).pack(pady=20)

    # 确认按钮
    tk.Button(
        limit_window,
        text="确定",
        command=limit_window.destroy,
        font=("微软雅黑", 10),
        width=10
    ).pack(pady=10)

    limit_window.mainloop()