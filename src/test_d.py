import usb.core
import usb.util
import time


def get_usb_devices():
    devices = []
    for device in usb.core.find(find_all=True):
        try:
            # 获取设备描述
            manufacturer = usb.util.get_string(device, device.iManufacturer)
            product = usb.util.get_string(device, device.iProduct)

            devices.append({
                "vendor_id": f"{device.idVendor:04x}",
                "product_id": f"{device.idProduct:04x}",
                "manufacturer": manufacturer,
                "product": product
            })
        except (usb.core.USBError, ValueError):
            continue  # 忽略无法访问的设备
    return devices


# # 监控设备变化
# if __name__ == "__main__":
#     known_devices = set()

    while True:
        current_devices = set()
        for device in get_usb_devices():
            device_id = f"{device['vendor_id']}:{device['product_id']}"
            current_devices.add(device_id)

            if device_id not in known_devices:
                print(f"新设备: {device['manufacturer']} {device['product']}")

        known_devices = current_devices
        time.sleep(1)