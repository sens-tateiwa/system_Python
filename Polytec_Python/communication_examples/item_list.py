#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import argparse
import logging
import os.path as path
import sys

from polytec.io.device_command import DeviceCommand
from polytec.io.device_communication import DeviceCommunication
from polytec.io.device_type import DeviceType
from polytec.io.item_list import ItemList


def user_input_to_enum_id(user_input, enum_values):
    try:
        return int(user_input)
    except ValueError:
        try:
            return enum_values[user_input]
        except KeyError:
            logging.error(f"{user_input} is not a valid device or command")
            sys.exit(1)


def parse_cli_args():
    """Defines and handles the command-line interface."""
    usage_example_text = f'''usage examples:

      python {path.basename(__file__)} 192.168.0.10 VelocityDecoderDigital Range
    '''

    cli_parser = argparse.ArgumentParser(description='Item list commands usage example.',
                                         epilog=usage_example_text,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

    # define the command-line interface
    cli_parser.add_argument("address",
                            help="IPv4 or hostname of the device to connect to")
    cli_parser.add_argument("device",
                            help="The logical device to use (e.g. 7 or \"VelocityDecoderDigital\"")
    cli_parser.add_argument("command",
                            help="The device command to use (e.g. 10 or \"Range\"")
    cli_parser.add_argument("-l, --logging-level",
                            dest="logging_level",
                            help="Logging level",
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            default="WARNING")

    cli_args = cli_parser.parse_args()

    # set logging level
    logging.basicConfig(level=cli_args.logging_level, format="%(asctime)-15s [%(levelname)s] %(message)s")

    device_type = DeviceType(int(cli_args.device)) if cli_args.device.isnumeric() else DeviceType[cli_args.device]
    command = DeviceCommand(int(cli_args.command)) if cli_args.command.isnumeric() else DeviceCommand[cli_args.command]

    # set global variables
    return cli_args.address, device_type, command


# [main]
def main():
    """Main functionality"""
    try:
        device_ip, device_type, command = parse_cli_args()

        # initialize Device Communication and connect to a device
        device_communication = DeviceCommunication(device_ip)

        # item list functions demonstration
        # also take a look at get_all_items and is_item_available for more item list functions
        item_list = ItemList(device_communication, device_type, command)
        available_items = item_list.available_items()
        print("Available items:", ", ".join(available_items))
        print("Current item:", item_list.current_item())
        print(80*"-")
        new_item = input("Specify new item to be set: ").strip()
        if new_item in available_items:
            item_list.set_current_item(new_item)
            print(f"Successfully set current item to \"{new_item}\"")
        else:
            logging.error(f"\"{new_item}\" is not a valid available item to be set")
            sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [main]


if __name__ == "__main__":
    main()
