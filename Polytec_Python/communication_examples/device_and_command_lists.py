#!/usr/bin/env python3
# Copyright (c) 2020-2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import argparse
import logging
import os.path as path
import sys

from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication, UnableToLoadDllError, LibraryFunctionCallError
from polytec.io.device_type import DeviceType

__name_not_found = "[enum name not found]"


def parse_cli_args():
    """Defines and handles the command-line interface."""
    usage_example_text = f'''usage examples:

      python {path.basename(__file__)} 192.168.0.10
    '''

    cli_parser = argparse.ArgumentParser(description='Fetch all logical devices and their supported device commands '
                                                     'from a Polytec device and print them to the commandline in '
                                                     'Markdown format.',
                                         epilog=usage_example_text,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

    # define the command-line interface
    cli_parser.add_argument("address",
                            help="IPv4 or hostname of the device to connect to")
    cli_parser.add_argument("-l, --logging-level",
                            dest="logging_level",
                            help="Logging level",
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            default="WARNING")

    cli_args = cli_parser.parse_args()

    # set logging level
    logging.basicConfig(level=cli_args.logging_level, format="%(asctime)-15s [%(levelname)s] %(message)s")

    # set global variables
    return cli_args.address


def print_heading(heading, level=1, underline=True):
    """
    Prints a Markdown heading to stdout

    Args:
        heading:    Content of the heading
        level:      Heading level (e.g. 1 for h1, 3 for h3)
        underline:  Underline the Heading instead of preceding it with number signs (#).
                    Only available with level 1 and 2
    """
    if not underline or level > 2:
        print("#" * level, end=" ")
    print(heading)
    if underline and level <= 2:
        print(("=" if level == 1 else "-") * len(heading))
    print()


def print_supported_devices_table(supported_device_ids):
    """
    Print all supported devices as a markdown table

    Args:
        supported_device_ids:   List of all logical device IDs supported by the device
    """
    print_heading("Supported Devices")
    # print table header
    print("ID   | Device\n-----|" + "-" * 44)
    # print table lines
    all_device_ids = set(item.value for item in DeviceType)
    for device_id in supported_device_ids:
        device_name = DeviceType(device_id).name if device_id in all_device_ids else __name_not_found
        print(f"{device_id:<5}| {device_name}")
    # print two line spacer
    print("\n")


def print_supported_commands_table(command_ids):
    """
    Print all supported commands as a markdown table

    Args:
        command_ids:        List of all command IDs supported by a logical device
    """
    # print table header
    print("ID   | Command\n-----|" + "-" * 44)
    # print table lines
    all_command_ids = set(item.value for item in DeviceCommand)
    for command_id in command_ids:
        command_name = DeviceCommand(command_id).name if command_id in all_command_ids else __name_not_found
        print(f"{command_id:<5}| {command_name}")
    # print two line spacer
    print("\n")


# [main]
def main():
    """Main functionality"""

    try:
        device_ip = parse_cli_args()

        # initialize Device Communication and connect to a device
        device_communication = DeviceCommunication(device_ip)

        # fetch and print the list of all logical devices supported by this device
        device_list = device_communication.get_int16(DeviceType.Controller, DeviceCommand.DeviceList,
                                                     max_value_count=100)
        print_supported_devices_table(device_list)

        # fetch and print the list of all commands supported for each logical device
        print_heading("Supported commands for each device")
        for device_id in device_list:
            # print device header
            all_device_ids = set(item.value for item in DeviceType)
            device_type = DeviceType(device_id) if device_id in all_device_ids else f"Device {device_id}"
            print_heading(device_type, level=2, underline=False)

            # get the list of all supported commands for this logical device
            command_ids = device_communication.get_int16(device_id, DeviceCommand.CommandList, max_value_count=100)
            print_supported_commands_table(command_ids)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [main]


if __name__ == "__main__":
    main()
