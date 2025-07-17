import wmi
import time

def get_usb_devices():
    c = wmi.WMI()
    devices = []
    for usb in c.Win32_PnPEntity():
        if "USB" in str(usb):
            if usb.Name and usb.DeviceID:
                devices.append((usb.Name, usb.DeviceID))
    return devices

def monitor_usb():
    print("开始监控 USB 设备变化...")
    previous_devices = set(get_usb_devices())

    while True:
        current_devices = set(get_usb_devices())
        added = current_devices - previous_devices
        removed = previous_devices - current_devices

        for dev in added:
            print(f"[插 入] {dev[0]} (DeviceID: {dev[1]})")

        for dev in removed:
            print(f"[拔 出] {dev[0]} (DeviceID: {dev[1]})")

        previous_devices = current_devices
        time.sleep(2)

# if __name__ == "__main__":
#     monitor_usb()