
import logger_config
import check_launch
import tkinter as tk

# main.py
import threading
import interface
from tray_icon import create_tray_icon

if __name__ == "__main__":
    logger_config.setup_logger()

    if check_launch.check_launch_limit():
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        # 显示密码窗口（此时才创建 password_window 和 app_window）
        interface.show_password_window()

        # 使用 lambda 延迟获取窗口对象
        tray_thread = threading.Thread(
            target=create_tray_icon,
            args=(root, lambda: interface.password_window, lambda: interface.app_window),
            daemon=True
        )
        tray_thread.start()

        root.mainloop()
