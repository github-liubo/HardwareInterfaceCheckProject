# tray_icon.py
import pystray
from PIL import Image
import os


def create_tray_icon(root, get_password_window, get_app_window):
    def on_restore(icon, item):
        password_window = get_password_window()
        app_window = get_app_window()

        if app_window and app_window.winfo_exists():
            app_window.deiconify()
        elif password_window and password_window.winfo_exists():
            password_window.deiconify()

    def on_exit(icon, item):
        icon.stop()
        root.quit()
        root.destroy()

    def create_image():
        # 路径逻辑：当前文件（tray_icon.py）所在目录 → 上级目录 → assets/images/目标文件
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),  # 当前文件目录（如 src/）
            os.pardir,  # 上级目录（src的父目录）
            "assets", "images", "detection.jpg"
        )
        icon_path = os.path.normpath(icon_path)  # 标准化路径（关键：处理 ../ 符号）

        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"图标文件不存在：{icon_path}")

        return Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem("打开", on_restore),
        pystray.MenuItem("退出", on_exit)
    )

    icon = pystray.Icon("HardwareChecker", create_image(), "硬件检测工具", menu)
    icon.run()