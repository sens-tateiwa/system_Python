#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.


# This example script streams the acquired data directly of a device without any trigger handling (trigger options are
# only available in block mode). Note that data streaming data can lead to buffer overflows within the device when used
# with high bandwidths and/or a large number of active channels as the throughput might be limited by the bandwidth of
# your network connection.

# See print_config_options.py to determine your devices configuration options.
# See interactive_channel_selection.py to select the active acquisition channels.
# See interactive_bandwidth_and_range.py to select the bandwidth and ranges used for the data acquisition.

import logging
import sys

from polytec.io.device_communication import DeviceCommunication

from .acquisition_control.config import DaqConfig
from .acquisition_control import acquireData


def prepare():
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(message)s")

    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print(f"usage: {sys.argv[0]} address")
        sys.exit(1)
    return sys.argv[1]


# [run]
def run(address, sample_count=10000):
    try:
        device_communication = DeviceCommunication(address)

        # configure acquisition
        config = DaqConfig(device_communication)
        config.daq_mode = "Streaming"

        # perform acquisition of 10000 base samples (samples in lowest common denominator sample rate of all channel)
        data = acquireData.acquire_data(device_communication, sample_count)
    except Exception as e:
        logging.error(e)
        #data = "something wrong in acquire_streaming.run"
        data = 0
        #sys.exit(1)
    #print("acquire_streaming.run was done")
    return data
# [run]


if __name__ == "__main__":
    ip_address = prepare()
    sample_count = 2**18 #2^18 = 262,144
    run(ip_address, sample_count)
