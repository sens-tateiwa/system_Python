#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.


# This example script configures and preforms a block acquisition with an analog trigger. Block acquisition is only
# available on some devices (e.g. VFX-F-110). In block acquisition data is acquired and delivered in blocks of data and
# not in a continuous stream. Block acquisition can be especially useful if the bandwidth of your connection to the
# device is lower than the bandwidth of the acquired signal, as the complete data block is guaranteed to be able to be
# buffered on the device itself, while being delivered over the slower connection.

# Using block acquisition also enables the use of the trigger settings. If a trigger is enabled, the trigger will have
# to fire for each block individually.

# See print_config_options.py to determine your devices configuration options (e.g. block acquisition support)
# See interactive_channel_selection.py to select the active acquisition channels.
# See interactive_bandwidth_and_range.py to select the bandwidth and ranges used for the data acquisition.

import logging
import sys

from polytec.io.device_communication import DeviceCommunication

from acquisition_control.config import DaqConfig
from acquisition_control import acquire_to_csv


def prepare():
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(message)s")

    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print(f"usage: {sys.argv[0]} address")
        sys.exit(1)
    return sys.argv[1]


# [run]
def run(address):
    try:
        device_communication = DeviceCommunication(address)

        # configure acquisition
        daq_config = DaqConfig(device_communication)
        daq_config.daq_mode = "Block"  # not supported by every device (e.g. IVS-500 and VGO-200)
        daq_config.block_size = 10000  # base samples (samples in lowest common denominator sample rate of all channels)
        daq_config.block_count = 3
        daq_config.trigger_mode = "Analog"
        daq_config.trigger_edge = "Rising"
        daq_config.analog_trigger_level = 0.0  # value between -1 and 1
        daq_config.pre_post_trigger = 2000  # actual signal channel samples not base samples

        # perform acquisition
        acquire_to_csv.acquire_data(device_communication)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [run]


if __name__ == "__main__":
    ip_address = prepare()
    run(ip_address)
