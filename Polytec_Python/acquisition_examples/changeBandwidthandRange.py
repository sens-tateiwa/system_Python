
#changeBandwidthandRange
#examles/Python/acquisition examples/interactive_bandwidth_and_range_selection.py参照

import logging
import sys

from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication
from polytec.io.device_type import DeviceType
from polytec.io.item_list import ItemList


# [bandwidth_selection]
"""
Available items: 100 kHz, 50 kHz, 25 kHz, 10 kHz, 5 kHz, 1 kHz
"""
def changeBandwidth(device_communication, new_bandwidth):
    bandwidth_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Bandwidth)
    if len(new_bandwidth) > 0:
        bandwidth_list.set_current_item(new_bandwidth)
    # [bandwidth_selection]


# [range_selection]
"""
Available items: 2 m/s, 1 m/s, 500mm/s, 200 mm/s, 100 mm/s, 50 mm/s, 20 mm/s, 10 mm/s
"""
def changeRange(device_communication, new_range):
    range_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Range)
    if len(new_range) > 0:
        range_list.set_current_item(new_range)
    # [range_selection]



# [run]
def run(address, new_bandwidth="1 kHz", new_range="2 m/s"):
    try:
        device_communication = DeviceCommunication(address)
        print(f"new_bandwidth = {new_bandwidth}")
        print(f"new_range = {new_range}")
        changeBandwidth(device_communication, new_bandwidth)
        changeRange(device_communication, new_range)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [run]


if __name__ == "__main__":
    ip_address = "192.168.137.1"
    device_communication = DeviceCommunication(ip_address)

    bandwidth_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Bandwidth)
    available_bandwidths = bandwidth_list.available_items()
    print(f"Available bandwidths: {', '.join(available_bandwidths)}")
    if len(available_bandwidths) > 1:
        new_bandwidth = input(f"New bandwidth [{bandwidth_list.current_item()}]: ").strip()

    range_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Range)
    available_ranges = range_list.available_items()
    print(f"Available Velocity ranges: {', '.join(available_ranges)}")
    if len(available_ranges) > 1:
        new_range = input(f"New Velocity range [{range_list.current_item()}]: ").strip()
    
    run(ip_address, new_bandwidth, new_range)
