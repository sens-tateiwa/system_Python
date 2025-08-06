#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.


# This script allows the user to interactively select the bandwidth and channel ranges to be configured on a device.

import logging
import sys

from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication
from polytec.io.device_type import DeviceType
from polytec.io.item_list import ItemList


# [bandwidth_selection]
def interactive_bandwidth_selection(device_communication):
    bandwidth_list = ItemList(device_communication, DeviceType.VelocityDecoderDigital, DeviceCommand.Bandwidth)
    available_bandwidths = bandwidth_list.available_items()
    print(f"Available bandwidths: {', '.join(available_bandwidths)}")
    if len(available_bandwidths) > 1:
        new_bandwidth = input(f"New bandwidth [{bandwidth_list.current_item()}]: ").strip()
        if len(new_bandwidth) > 0:
            bandwidth_list.set_current_item(new_bandwidth)
    # [bandwidth_selection]


# [range_selection]
def interactive_range_selection(device_communication):
    for channel_name in ["Velocity", "Displacement", "Acceleration"]:
        decoder_device = DeviceType[f"{channel_name}DecoderDigital"]
        if device_communication.has_device(decoder_device):
            range_list = ItemList(device_communication, decoder_device, DeviceCommand.Range)
            available_ranges = range_list.available_items()
            print(f"Available {channel_name} ranges: {', '.join(available_ranges)}")
            if len(available_ranges) > 1:
                new_range = input(f"New {channel_name} range [{range_list.current_item()}]: ").strip()
                if len(new_range) > 0:
                    range_list.set_current_item(new_range)
    # [range_selection]


def prepare():
    logging.basicConfig(level=logging.WARNING, format="%(asctime)-15s [%(levelname)s] %(message)s")

    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print(f"usage: {sys.argv[0]} address")
        sys.exit(1)
    return sys.argv[1]


# [run]
def run(address):
    try:
        device_communication = DeviceCommunication(address)
        interactive_bandwidth_selection(device_communication)
        interactive_range_selection(device_communication)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [run]


if __name__ == "__main__":
    #ip_address = prepare()
    ip_address = "192.168.137.1"
    run(ip_address)
