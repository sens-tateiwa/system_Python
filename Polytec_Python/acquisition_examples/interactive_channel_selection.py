#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.


# This script allows the user to interactively select the channels active on a device.

# For Devices supporting the channel activation command (e.g. VFX-F-110) the ChannelActivation class is being used to
# configure all available channels (all channels can be enabled or disabled).

# For devices not supporting the channel activation the output active command is being used to select what signal
# channel should be active right now (Velocity, Displacement or Acceleration, based on channel availability or license).
# On this devices or channel types, like the RSSI or trigger channels cannot be disabled and are enabled all the time.

import logging
import sys

from polytec.io.channel_activation import ChannelActivation
from polytec.io.channel_type import ChannelType
from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication
from polytec.io.device_type import DeviceType
from acquisition_control.config import DaqConfig


# [channel_activation]
def interactive_channel_activation(device_communication):
    """Prompt the user for every currently available channel if it should be enabled or not"""

    channel_activation = ChannelActivation(device_communication)
    channel_activation.disable_all_channels()

    # Note: Channel availability can be affected by the data acquisition configuration as well as already enabled
    # channels (e.g. acceleration is not available on VFX-F-110 devices if the configured bandwidth is above 3 MHz)
    for channel_type in ChannelType:
        if channel_activation.is_channel_type_supported(channel_type):
            for channel_id in range(channel_activation.max_channel_count(channel_type)):
                if channel_activation.is_channel_available(channel_type, channel_id):
                    if "n" not in input(f"Enable {channel_type.name} channel {channel_id} [Y/n]: ").lower():
                        channel_activation.enable_channel(channel_type, channel_id)
    # [channel_activation]


# [output_active_selection]
def interactive_output_active_selection(daq_config):
    """Prompt the user to select one of the available active output channels"""

    available_outputs = daq_config.available_active_outputs()
    print(f"Currently active output: {daq_config.active_output.name}")
    print(f"Available active output channels: {', '.join(channel.name for channel in available_outputs)}")
    if len(available_outputs) > 1:
        daq_config.active_output = ChannelType[input(f"New active output: ").capitalize()]
    # [output_active_selection]


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

        # interactive channel selection
        if len(daq_config.available_active_outputs()) > 0:
            interactive_output_active_selection(daq_config)
        elif device_communication.has_command(DeviceType.SignalProcessing, DeviceCommand.DaqActiveChannels):
            interactive_channel_activation(device_communication)
        else:
            logging.error("The device neither supports the output active, nor the channel activation command")
            sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [run]


if __name__ == "__main__":
    ip_address = prepare()
    run(ip_address)
