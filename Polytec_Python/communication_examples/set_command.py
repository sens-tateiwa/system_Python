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


def parse_cli_args():
    """Defines and handles the command-line interface."""
    usage_example_text = f'''usage examples:

      python {path.basename(__file__)} 192.168.0.10 18 934 float 0.23           # set analog trigger level
      python {path.basename(__file__)} 192.168.0.10 SensorHead LaserOn int16 1  # turn laser on
    '''

    cli_parser = argparse.ArgumentParser(description='Send a set command to a Polytec device using the device command, '
                                                     'logical device and value specified.',
                                         epilog=usage_example_text,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

    # define the command-line interface
    cli_parser.add_argument("address",
                            help="IPv4 or hostname of the device to connect to")
    cli_parser.add_argument("device",
                            help="The logical device to use (e.g. 2 or \"SensorHead\"")
    cli_parser.add_argument("command",
                            help="The device command to use (e.g. 46 or \"LaserOn\"")
    cli_parser.add_argument("payload_type",
                            help="The Type of the device command payload (following types are supported: "
                                 "int16, int32, float, string)")
    cli_parser.add_argument("value",
                            help="The value to be set")
    cli_parser.add_argument("-l, --logging-level",
                            dest="logging_level",
                            help="Logging level",
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            default="WARNING")
    cli_args = cli_parser.parse_args()

    # set logging level
    logging.basicConfig(level=cli_args.logging_level, format="%(asctime)-15s [%(levelname)s] %(message)s")

    value = cli_args.value
    device_type = DeviceType(int(cli_args.device)) if cli_args.device.isnumeric() else DeviceType[cli_args.device]
    command = DeviceCommand(int(cli_args.command)) if cli_args.command.isnumeric() else DeviceCommand[cli_args.command]
    payload_type = cli_args.payload_type.lower()

    return cli_args.address, device_type, command, payload_type, value


# [main]
def main():
    """Main functionality"""
    try:
        device_ip, device_type, command, payload_type, value = parse_cli_args()

        # initialize Device Communication and connect to a device
        device_communication = DeviceCommunication(device_ip)

        # send set command
        if payload_type == "int16":
            device_communication.set_int16(device_type, command, int(value))
        elif payload_type == "int32":
            device_communication.set_int32(device_type, command, int(value))
        elif payload_type == "float":
            device_communication.set_float(device_type, command, float(value))
        elif payload_type == "string":
            device_communication.set_string(device_type, command, value)
        else:
            logging.error(f"{payload_type} is not a supported command type")
            sys.exit(1)

        print(f"Command value successfully set to \"{value}\"")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    # [main]


if __name__ == "__main__":
    main()
