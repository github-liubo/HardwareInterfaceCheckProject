import logger_config
import check_launch
import interface

if __name__ == "__main__":
    logger_config.setup_logger()
    if check_launch.check_launch_limit():
        interface.show_password_window()