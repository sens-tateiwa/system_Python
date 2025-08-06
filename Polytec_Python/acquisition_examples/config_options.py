#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

# This example script determines your devices configuration options (e.g. block acquisition support)

import logging
import sys

from polytec.io.channel_type import ChannelType
from polytec.io.channel_activation import ChannelActivation
from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication
from polytec.io.device_type import DeviceType

from acquisition_control.config import DaqConfig


def prepare():
    logging.basicConfig(level=logging.WARNING, format="%(asctime)-15s [%(levelname)s] %(message)s")

    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print(f"usage: {sys.argv[0]} address")
        sys.exit(1)
    return sys.argv[1]


# [run]
def run(address):
    try:
        # prepare communication
        device_communication = DeviceCommunication(address)
        daq_config = DaqConfig(device_communication)
        channel_activation = ChannelActivation(device_communication)

        # read and print configuration options
        daq_modes = daq_config.available_daq_modes()
        print(f"Data acquisition modes:         {', '.join(daq_modes)}")
        if "Block" in daq_modes:
            print(f"Block count range:              {daq_config.block_count_range()}")
            print(f"Block size range:               {daq_config.block_size_range()}")
            print(f"Trigger modes:                  {', '.join(daq_config.available_trigger_modes())}")
            print(f"Trigger edges:                  {', '.join(daq_config.available_trigger_edges())}")
            print(f"Analog trigger sources:         {', '.join(daq_config.available_analog_trigger_sources())}")
            print(f"Analog trigger level range:     {daq_config.analog_trigger_level_range()}")
            print(f"Pre-/Post-trigger range:        {daq_config.pre_post_trigger_range()}")
        print(f"Active output supported:        {len(daq_config.available_active_outputs()) > 0}")
        print(f"Channel activation supported:   "
              f"{device_communication.has_command(DeviceType.SignalProcessing, DeviceCommand.DaqActiveChannels)}")
        print("Supported channels:")
        for channel_type in ChannelType:
            if channel_activation.is_channel_type_supported(channel_type):
                print(f"\t{channel_type.name}",
                      ','.join(str(channel_id) for channel_id in range(channel_activation.max_channel_count(channel_type))))
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [run]


if __name__ == "__main__":
    ip_address = prepare()
    run(ip_address)
