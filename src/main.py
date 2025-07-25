
import logger_config
import check_launch
import tkinter as tk
import threading
import interface
from tray_icon import create_tray_icon
import importlib
import interface as interface_module
importlib.reload(interface_module)  # 可选：强制重新加载模块

if __name__ == "__main__":
    logger_config.setup_logger()

    if check_launch.check_launch_limit():
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        # 使用字典来包装变量，以便在嵌套函数中修改
        gui_state = {
            "initialized": False
        }

        # 定义回调函数，用于USB事件触发硬件检测
        def usb_event_callback():
            if gui_state["initialized"]:
                interface.app_window.after(0, interface.detect_hardware)

        # 启动 USB 监听线程
        from usb_monitor import main as start_usb_monitoring
        usb_monitor_thread = threading.Thread(
            target=start_usb_monitoring,
            args=(usb_event_callback,),
            daemon=True
        )
        usb_monitor_thread.start()

        # 显示密码窗口（此时才创建 password_window 和 app_window）
        interface.show_password_window()
        gui_state["initialized"] = True  # 修改状态为已初始化

        # 启动托盘图标线程
        tray_thread = threading.Thread(
            target=create_tray_icon,
            args=(root, lambda: interface.password_window, lambda: interface.app_window),
            daemon=True
        )
        tray_thread.start()

        root.mainloop()