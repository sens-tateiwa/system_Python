"""
@package io
"""

# Copyright (c) 2020-2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import ipaddress
import logging
import os.path as path
import pkg_resources
import socket
import sys
from ctypes import *

from polytec.io.communication_status_code import CommunicationStatusCode
from polytec.io.miscellaneous_tag import MiscellaneousTag


def check_success(function_name, status_code):
    if status_code != CommunicationStatusCode.Success:
        raise LibraryFunctionCallError(function_name, status_code)


class ClassProperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class DeviceCommunication:
    """Device communication interface Python wrapper"""

    # class variables
    __device_communication_dll = None
    __dll_path = ""
    __instance_count = 0

    def __init__(self, device_address, timeout_ms=2000, dll_path=None):
        """
        Constructor

        Initializes the instance and loads the Device Communication DLL to a class variable (if not already loaded by
        another instance).

        Args:
            dll_path:       Path to the Device Communication DLL to be used
            device_address: The IP address or hostname of the Polytec device
            timeout_ms:     Communication timeout in milliseconds

        Raises:
            UnableToLoadDllError, TypeError, LibraryFunctionCallError
        """
        # initialize instance variables
        self.__communication_handle = None
        # load the Device Communication DLL
        self.__load_dll(dll_path)
        self.__open_connection(device_address, timeout_ms)

    @ClassProperty
    def device_communication_dll(cls):
        """Access the device communication dll"""
        return cls.__device_communication_dll

    def __del__(self):
        """Destructor"""
        self.__close_connection()
        self.__unload_dll()

    @property
    def communication_handle(self):
        """Get the communication handle"""
        return self.__communication_handle

    @staticmethod
    def last_error():
        """
        Evaluates the last status message of the last Device Communication interface call

        Returns:
            The status message for the last error
        """
        assert DeviceCommunication.device_communication_dll is not None

        # void PolyLastCommunicationStatus(char* message, size_t bufferSize)
        poly_last_communication_status \
            = DeviceCommunication.device_communication_dll.PolyLastCommunicationStatus
        poly_last_communication_status.restype = None
        poly_last_communication_status.argtypes = [POINTER(c_char), c_long]

        # ctypes function parameter initialization
        c_message = create_string_buffer(2000)
        c_buffer_size = c_long(2000)

        logging.debug(f"Library call: PolyCommunicationStatusMessage({c_message}, {c_buffer_size})")
        poly_last_communication_status(c_message, c_buffer_size)

        return c_message.value.decode()

    @classmethod
    def __load_dll(cls, dll_path):
        """
        Load the Device Communication DLL to a class variable

        Args:
            dll_path:   Absolute path to the Device Communication DLL to be used

        Raises:
            UnableToLoadDllError
        """
        if not dll_path:
            default_dll_name = f"DeviceCommunication{'64' if sys.maxsize > 2 ** 32 else '32'}.dll"
            if pkg_resources.resource_exists("polytec.resources", default_dll_name):
                dll_path = pkg_resources.resource_filename("polytec.resources", default_dll_name)
            else:
                raise UnableToLoadDllError("No device communication DLL could be found. "
                                           "Please specify specific file path to the DLL.")

        if cls.device_communication_dll is None:
            try:
                cls.__dll_path = path.abspath(dll_path)
                cls.device_communication_dll = cdll.LoadLibrary(cls.__dll_path)
                logging.debug(f"Successfully loaded \"{dll_path}\"")
            except OSError as e:
                cls.device_communication_dll = None
                raise UnableToLoadDllError(f"Failed to load \"{dll_path}\"") from e
        elif dll_path != cls.__dll_path:
            raise UnableToLoadDllError(f"Cannot load \"{dll_path}\". "
                                       f"A different DLL has already been loaded: \"{cls.__dll_path}\"")
        cls.__instance_count += 1

    @classmethod
    def __unload_dll(cls):
        """Make sure the DLL is marked to be freed by GC as soon as all instances of this class have been destructed"""
        cls.__instance_count -= 1
        logging.debug(f"Device Communication instance count decreased. New value: {cls.__instance_count}")
        if cls.__instance_count == 0:
            logging.debug(f"Last Device Communication instance deleted. "
                          f"Marking Device Communication DLL to be freed by GC.")
            cls.device_communication_dll = None
            cls.__dll_path = ""

    def __open_connection(self, device_address, timeout_ms=2000):
        """
        Open a TCP connection for the device communication with a Polytec device (e.g. IVS-500)

        Args:
            device_address: The IP address or hostname of the Polytec device
            timeout_ms:     Communication timeout in milliseconds

        Raises:
            TypeError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        try:
            # get IP from hostname / validate IP address format
            device_ip = ipaddress.IPv4Address(socket.gethostbyname(device_address))
        except (socket.herror, socket.gaierror, ipaddress.AddressValueError) as e:
            raise TypeError(f"\"{device_address}\" is not a valid IPv4 address or hostname") from e

        # int PolyOpenTcpEthernetCommunication(int* communicationHandle, const char* ipAddress, int timeoutInMs)
        # [define_signature]
        poly_open_tcp_ethernet_communication \
            = DeviceCommunication.device_communication_dll.PolyOpenTcpEthernetCommunication
        poly_open_tcp_ethernet_communication.restype = c_int
        poly_open_tcp_ethernet_communication.argtypes = [POINTER(c_int), c_char_p, c_int]
        # [define_signature]

        # ctypes function parameter initialization
        # [prepare_arguments]
        self.__communication_handle = c_int()
        c_ip = c_char_p(str(device_ip).encode())
        c_timeout_in_ms = c_int(timeout_ms)
        # [prepare_arguments]

        logging.debug(f"Library call: PolyOpenTcpEthernetCommunication"
                      f"({byref(self.__communication_handle)}, {c_ip}, {c_timeout_in_ms})")
        # [library_function_call]
        status_code = poly_open_tcp_ethernet_communication(byref(self.__communication_handle), c_ip, c_timeout_in_ms)
        # [library_function_call]

        # [check_status_code]
        if status_code != CommunicationStatusCode.Success:
            self.__communication_handle = None
            raise LibraryFunctionCallError("PolyOpenTcpEthernetCommunication", status_code)
        # [check_status_code]

        logging.info(f"Successfully connected to the device: {device_ip}")

    def __close_connection(self):
        """Close the connection to the Polytec device (if open)"""
        if self.__communication_handle is not None:
            assert DeviceCommunication.device_communication_dll is not None

            # void PolyCloseCommunication(int communicationHandle)
            poly_close_communication = DeviceCommunication.device_communication_dll.PolyCloseCommunication
            poly_close_communication.argtypes = [c_int]

            poly_close_communication(self.__communication_handle)
            logging.info(f"Connection to the device closed")

    @staticmethod
    def __free_payload(payload_handle):
        # void PolyFreePayload(int payloadHandle)
        poly_free_payload = DeviceCommunication.device_communication_dll.PolyFreePayload
        poly_free_payload.argtypes = [c_int]

        logging.debug(f"Library call: PolyFreePayload({payload_handle})")
        poly_free_payload(payload_handle)

    def __set_low_level(self, device_type, device_command, poly_dll_payload_function, value_type, values,
                        miscellaneous_tag=None, device_number=0):
        """
        Set multiple values on the connected device via the device communication interface

        The value to be set will be determined by the device type and device command provided.
        In contrast the high level set method above, this method also supports multiple values and the
        miscellaneous tag, providing additional information for some commands. In order to achieve this the low level
        API has to be utilized.

        Low level API is used over high level commands to enable the use of miscellaneous tags and to allow multiple
        values to be set.

        Args:
            device_type:                The logical device to set the data on (see device_type.py)
            device_command:             The device command to be used for this operation (see device_command.py)
            poly_dll_payload_function:  The low level DLL function to be used to create the payload handle from the
                                        values (e.g. PolyCreatePayloadFromInt16)
            value_type:                 The type of the value to be set (e.g. c_int16, c_float)
            values:                     Values to be set on the device
            miscellaneous_tag:          Additional information for some commands (optional)
            device_number:              The device number, e.g. 0.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError, TypeError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # assert that values is a list
        if type(values) is not list:
            values = [values]

        # e.g. int PolyCreatePayloadFromInt16(const int16_t* value, size_t size)
        poly_dll_payload_function.restype = c_int
        poly_dll_payload_function.argtypes = [POINTER(value_type * len(values)), c_long]

        # ctypes function parameter initialization
        try:
            c_values = (value_type * len(values))(*values)
        except TypeError as e:
            raise TypeError(f"Unable to convert provided values {values} to {value_type.__name__}") from e
        c_value_count = c_long(len(values))

        logging.debug(f"Library call: PolyCreatePayloadFrom[{value_type.__name__}]({c_values}, {c_value_count}")
        c_payload_handle = poly_dll_payload_function(c_values, c_value_count)

        # int PolySendSetWithTag(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                        int tag, int payload)
        poly_send_set_with_tag = DeviceCommunication.device_communication_dll.PolySendSetWithTag
        poly_send_set_with_tag.restype = c_int
        poly_send_set_with_tag.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_miscellaneous_tag = c_int(miscellaneous_tag if miscellaneous_tag is not None
                                    else MiscellaneousTag.NoTag)

        logging.debug(f"Library call: PolySendSetWithTag({self.__communication_handle}, {c_device_type}, "
                      f"{c_device_number}, {c_device_command}, {c_miscellaneous_tag}, {c_payload_handle})")
        status_code = poly_send_set_with_tag(self.__communication_handle, c_device_type, c_device_number,
                                             c_device_command, c_miscellaneous_tag, c_payload_handle)
        check_success("PolySendSetWithTag", status_code)

        self.__free_payload(c_payload_handle)

    def __get_low_level(self, device_type, device_command, poly_dll_payload_function, return_type, max_value_count,
                        miscellaneous_tag=None, device_number=0):
        """
        Fetch multiple values from the device connected to via the device communication low level interface

        The values to be fetched will be determined by the device type and device command provided.
        In contrast the high level get method above, this method also supports multiple values and the
        miscellaneous tag, providing additional information for some commands. In order to achieve this the low level
        API has to be utilized.

        Low level API is used over high level commands to enable the use of miscellaneous tags and to allow multiple
        values to be fetched.

        Args:
            device_type:                The logical device to fetch the data from (see device_type.py)
            device_command:             The device command to be used for this operation (see device_command.py)
            poly_dll_payload_function:  The low level DLL function to be used to get the values from the payload handle
                                        (e.g. PolyGetInt16FromPayload)
            return_type:                The type of the value to be fetched from the device (e.g. c_int16, c_float)
            max_value_count:            The maximum amount of values to be returned (receive buffers will be sized
                                        accordingly). Amount of values returned will be less then or equal this value
            miscellaneous_tag:          Additional information for some commands (optional)
            device_number:              The device number, e.g. 0.

        Returns:
            A list of values fetched from the logical device provided

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolySendGetWithTag(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                        int tag, int* payload)
        poly_send_get_with_tag = DeviceCommunication.device_communication_dll.PolySendGetWithTag
        poly_send_get_with_tag.restype = c_int
        poly_send_get_with_tag.argtypes = [c_int, c_int, c_int, c_int, c_int, POINTER(c_int)]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_miscellaneous_tag = c_int(miscellaneous_tag if miscellaneous_tag is not None
                                    else MiscellaneousTag.NoTag)
        c_payload_handle = c_int()

        logging.debug(f"Library call: PolySendGetWithTag({self.__communication_handle}, {c_device_type}, "
                      f"{c_device_number}, {c_device_command}, {c_miscellaneous_tag}, {byref(c_payload_handle)})")
        status_code = poly_send_get_with_tag(self.__communication_handle, c_device_type, c_device_number,
                                             c_device_command, c_miscellaneous_tag, byref(c_payload_handle))
        check_success("PolySendGetWithTag", status_code)

        c_value_arr = return_type * max_value_count

        # e.g. int PolyGetInt16FromPayload(int payloadHandle, int16_t* payloadBuffer, size_t* payloadSize,
        #                                  size_t bufferSize)
        poly_dll_payload_function.restype = c_int
        poly_dll_payload_function.argtypes = [c_int, POINTER(c_value_arr), POINTER(c_long), c_long]

        # ctypes function parameter initialization
        c_values = c_value_arr()
        c_payload_size = c_long()
        c_buffer_size = c_long(max_value_count)

        logging.debug(f"Library call: PolyGet[{return_type.__name__}]FromPayload"
                      f"({c_payload_handle}, {byref(c_values)}, {byref(c_payload_size)}, {c_buffer_size})")
        status_code = poly_dll_payload_function(c_payload_handle, byref(c_values), byref(c_payload_size),
                                                c_buffer_size)
        check_success(f"PolyGet[{return_type.__name__}]FromPayload", status_code)

        self.__free_payload(c_payload_handle)

        logging.debug(f"{max_value_count} {return_type.__name__} values fetched from device {device_type} "
                      f"using command {device_command}")

        # convert ctype to python type
        return [c_values[i] for i in range(c_payload_size.value)] if max_value_count > 1 else c_values[0]

    def set_int16(self, device_type, device_command, values, miscellaneous_tag=None):
        """
        Set int16 value on the connected device via the device communication interface

        The value to be set will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to set the data on (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            values:                 Values to be set on the device
            miscellaneous_tag:      Additional information for some commands (optional)

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError, TypeError
        """
        self.__set_low_level(device_type, device_command,
                             DeviceCommunication.device_communication_dll.PolyCreatePayloadFromInt16,
                             c_int16, values, miscellaneous_tag=miscellaneous_tag)

    def get_int16(self, device_type, device_command, max_value_count=1, miscellaneous_tag=None):
        """
        Fetch int16 values from the connected device via the device communication interface

        The value to be fetched will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to fetch the data from (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            max_value_count:        The maximum amount of values to be returned (receive buffers will be sized
                                    accordingly). Amount of values returned will be less then or equal this value
            miscellaneous_tag:      Additional information for some commands (optional)

        Returns:
            A value fetched from the logical device provided

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        return self.__get_low_level(device_type, device_command,
                                    DeviceCommunication.device_communication_dll.PolyGetInt16FromPayload,
                                    c_int16, max_value_count, miscellaneous_tag=miscellaneous_tag)

    def set_float(self, device_type, device_command, values, miscellaneous_tag=None):
        """
        Set float value on the connected device via the device communication interface

        The value to be set will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to set the data on (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            values:                 Values to be set on the device
            miscellaneous_tag:      Additional information for some commands (optional)

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError, TypeError
        """
        self.__set_low_level(device_type, device_command,
                             DeviceCommunication.device_communication_dll.PolyCreatePayloadFromFloat,
                             c_float, values, miscellaneous_tag=miscellaneous_tag)

    def get_float(self, device_type, device_command, max_value_count=1, miscellaneous_tag=None):
        """
        Fetch float value from the connected device via the device communication interface

        The value to be fetched will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to fetch the data from (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            max_value_count:        The maximum amount of values to be returned (receive buffers will be sized
                                    accordingly). Amount of values returned will be less then or equal this value
            miscellaneous_tag:      Additional information for some commands (optional)

        Returns:
            A value fetched from the logical device provided

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        return self.__get_low_level(device_type, device_command,
                                    DeviceCommunication.device_communication_dll.PolyGetFloatFromPayload,
                                    c_float, max_value_count, miscellaneous_tag=miscellaneous_tag)

    def set_int32(self, device_type, device_command, values, miscellaneous_tag=None):
        """
        Set int32 value on the connected device via the device communication interface

        The value to be set will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to set the data on (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            values:                 Values to be set on the device
            miscellaneous_tag:      Additional information for some commands (optional)

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError, TypeError
        """
        self.__set_low_level(device_type, device_command,
                             DeviceCommunication.device_communication_dll.PolyCreatePayloadFromInt32,
                             c_int32, values, miscellaneous_tag=miscellaneous_tag)

    def get_int32(self, device_type, device_command, max_value_count=1, miscellaneous_tag=None):
        """
        Fetch int32 value from the connected device via the device communication interface

        The value to be fetched will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to fetch the data from (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            max_value_count:        The maximum amount of values to be returned (receive buffers will be sized
                                    accordingly). Amount of values returned will be less then or equal this value
            miscellaneous_tag:      Additional information for some commands (optional)

        Returns:
            A value fetched from the logical device provided

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        return self.__get_low_level(device_type, device_command,
                                    DeviceCommunication.device_communication_dll.PolyGetInt32FromPayload,
                                    c_int32, max_value_count, miscellaneous_tag=miscellaneous_tag)

    def set_string(self, device_type, device_command, value, device_number=0):
        """
        Set string value on the connected device via the device communication interface

        The value to be set will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to set the data on (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            value:                  Value to be set on the device
            device_number:          The device number, e.g. 0.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        poly_send_set_string = DeviceCommunication.device_communication_dll.PolySendSetString
        poly_send_set_string.restype = c_int
        poly_send_set_string.argtypes = [c_int, c_int, c_int, c_int, c_char_p]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_value = c_char_p(value.encode('utf-8'))

        logging.debug(f"Library call: PolySendSetString({self.__communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {c_value})")
        status_code = poly_send_set_string(self.__communication_handle, c_device_type, c_device_number,
                                           c_device_command, c_value)
        check_success("PolySendSetString", status_code)

    def get_string(self, device_type, device_command, expect_length=100, device_number=0):
        """
        Fetch string value from the connected device via the device communication interface

        Args:
            device_type:            The logical device to fetch the data from (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            expect_length:          The expected length of the returned string
            device_number:          The device number, e.g. 0.

        Returns:
            A value fetched from the logical device provided

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolySendGetString(int communicationHandle, int deviceType, int deviceNumber,
        #                       int deviceCommand, char* payload, size_t bufferSize)
        poly_send_get_string = DeviceCommunication.device_communication_dll.PolySendGetString
        poly_send_get_string.restype = c_int
        poly_send_get_string.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_char), c_long]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_value_buffer = create_string_buffer(expect_length)
        c_buffer_size = c_long(expect_length)

        logging.debug(f"Library call: PolySendGetString({self.__communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {c_value_buffer}, {c_buffer_size})")
        status_code = poly_send_get_string(self.__communication_handle, c_device_type, c_device_number,
                                           c_device_command, c_value_buffer, c_buffer_size)
        check_success("PolySendGetString", status_code)

        return c_value_buffer.value.decode()

    def set_uint32(self, device_type, device_command, values, miscellaneous_tag=None):
        """
        Set uint32 values on the connected device via the device communication interface

        Args:
            device_type:            The logical device to set the data on (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            values:                 Value to be set on the device
            miscellaneous_tag:      Additional information for some commands (optional)

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError, TypeError
        """
        self.__set_low_level(device_type, device_command,
                             DeviceCommunication.device_communication_dll.PolyCreatePayloadFromUInt32,
                             c_uint32, values, miscellaneous_tag=miscellaneous_tag)

    def get_uint32(self, device_type, device_command, max_value_count=1, miscellaneous_tag=None):
        """
        Fetch uint32 values from the connected device via the device communication interface

        The value to be fetched will be determined by the device type and device command provided.

        Args:
            device_type:            The logical device to fetch the data from (see device_type.py)
            device_command:         The device command to be used for this operation (see device_command.py)
            max_value_count:        The maximum amount of values to be returned (receive buffers will be sized
                                    accordingly). Amount of values returned will be less then or equal this value
            miscellaneous_tag:      Additional information for some commands (optional)

        Returns:
            A value fetched from the logical device provided

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """

        return self.__get_low_level(device_type, device_command,
                                    DeviceCommunication.device_communication_dll.PolyGetUInt32FromPayload,
                                    c_uint32, max_value_count, miscellaneous_tag=miscellaneous_tag)

    def get_int16_range(self, device_type, device_command, device_number=0):
        """
        Sends a GetDevInfo-command to get the range of a 16 bit int value from a device (e.g. FocusPosition).

        Args:
            device_type:    The device type, e.g. Controller.
            device_command: The device command to be used for this operation (see device_command.py)
            device_number:  The device number, e.g. 0.

        Returns:
            Minimum and maximum values as a pair.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolySendGetDevInfoRange(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                             int16_t* minimum, int16_t* maximum)
        poly_send_get_dev_info_range = DeviceCommunication.device_communication_dll.PolySendGetDevInfoRange
        poly_send_get_dev_info_range.restype = c_int
        poly_send_get_dev_info_range.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_int16), POINTER(c_int16)]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_min = c_int16()
        c_max = c_int16()

        logging.debug(f"Library call: PolySendGetDevInfoRange({self.__communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {byref(c_min)}, {byref(c_max)})")
        status_code = poly_send_get_dev_info_range(self.__communication_handle, c_device_type, c_device_number,
                                                   c_device_command, byref(c_min), byref(c_max))
        check_success("PolySendGetDevInfoRange", status_code)

        return c_min.value, c_max.value

    def get_int32_range(self, device_type, device_command, device_number=0):
        """
        Sends a GetDevInfo-command to get the range of a 32 bit int value from a device (e.g. DaqBlockSize).

        Args:
            device_type:    The device type, e.g. Controller.
            device_command: The device command to be used for this operation (see device_command.py)
            device_number:  The device number, e.g. 0.

        Returns:
            Minimum and maximum values as a pair.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolySendGetDevInfo(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                        int* payloadHandle)
        poly_send_get_dev_info = DeviceCommunication.device_communication_dll.PolySendGetDevInfo
        poly_send_get_dev_info.restype = c_int
        poly_send_get_dev_info.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_int)]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_payload_handle = c_int()

        logging.debug(f"Library call: PolySendGetDevInfo({self.__communication_handle}, {c_device_type}, "
                      f"{c_device_number}, {c_device_command}, {byref(c_payload_handle)})")
        status_code = poly_send_get_dev_info(self.__communication_handle, c_device_type, c_device_number,
                                             c_device_command, byref(c_payload_handle))
        check_success("PolySendGetDevInfo", status_code)

        c_payload_buffer = c_int32 * 2

        # int PolyGetInt32FromPayload(int payloadHandle, int32_t* payloadBuffer, size_t* payloadSize,
        #                             size_t bufferSize)
        poly_get_int32_from_payload = DeviceCommunication.device_communication_dll.PolyGetInt32FromPayload
        poly_get_int32_from_payload.restype = c_int
        poly_get_int32_from_payload.argtypes = [c_int, POINTER(c_payload_buffer), POINTER(c_long), c_long]

        # ctypes function parameter initialization
        c_range = c_payload_buffer()
        c_payload_size = c_long()
        c_buffer_size = c_long(2)

        logging.debug(f"Library call: PolyGetInt32FromPayload({c_payload_handle}, {byref(c_range)}, "
                      f"{byref(c_payload_size)}, {c_buffer_size})")
        status_code = poly_get_int32_from_payload(c_payload_handle, byref(c_range), byref(c_payload_size),
                                                  c_buffer_size)
        check_success("PolyGetInt32FromPayload", status_code)

        self.__free_payload(c_payload_handle)

        return c_range[0], c_range[1]

    def get_float_range(self, device_type, device_command, device_number=0):
        """
        Sends a GetDevInfo-command to get the range of a floating point value from a device (e.g. DaqAnalogTriggerLevel)

        Args:
            device_type:    The device type, e.g. Controller.
            device_command: The device command to be used for this operation (see device_command.py)
            device_number:  The device number, e.g. 0.

        Returns:
            Minimum and maximum values as a pair.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolySendGetDevInfo(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                        int* payloadHandle)
        poly_send_get_dev_info = DeviceCommunication.device_communication_dll.PolySendGetDevInfo
        poly_send_get_dev_info.restype = c_int
        poly_send_get_dev_info.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_int)]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_payload_handle = c_int()

        logging.debug(f"Library call: PolySendGetDevInfo({self.__communication_handle}, {c_device_type}, "
                      f"{c_device_number}, {c_device_command}, {byref(c_payload_handle)})")
        status_code = poly_send_get_dev_info(self.__communication_handle, c_device_type, c_device_number,
                                             c_device_command, byref(c_payload_handle))
        check_success("PolySendGetDevInfo", status_code)

        c_payload_buffer = c_float * 2

        # int PolyGetInt32FromPayload(int payloadHandle, float* payloadBuffer, size_t* payloadSize,
        #                             size_t bufferSize)
        poly_get_float_from_payload = DeviceCommunication.device_communication_dll.PolyGetFloatFromPayload
        poly_get_float_from_payload.restype = c_int
        poly_get_float_from_payload.argtypes = [c_int, POINTER(c_payload_buffer), POINTER(c_long), c_long]

        # ctypes function parameter initialization
        c_range = c_payload_buffer()
        c_payload_size = c_long()
        c_buffer_size = c_long(2)

        logging.debug(f"Library call: PolyGetFloatFromPayload({c_payload_handle}, {byref(c_range)}, "
                      f"{byref(c_payload_size)}, {c_buffer_size})")
        status_code = poly_get_float_from_payload(c_payload_handle, byref(c_range), byref(c_payload_size),
                                                  c_buffer_size)
        check_success("PolyGetFloatFromPayload", status_code)

        self.__free_payload(c_payload_handle)

        return c_range[0], c_range[1]

    def has_device(self, device_type, device_number=0):
        """
        Check if a device is available (e.g. SensorHead 0).

        Args:
            device_type:    The device type, e.g. Controller.
            device_number:  The device number, e.g. 0.

        Returns:
            True if available, false if not.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyHasDevice(int communicationHandle, int deviceType, int deviceNumber, bool* result)
        poly_has_device = DeviceCommunication.device_communication_dll.PolyHasDevice

        poly_has_device.restype = c_int
        poly_has_device.argtypes = [c_int, c_int, c_int, POINTER(c_bool)]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_result = c_bool()

        logging.debug(f"Library call: PolyHasDevice({self.__communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {byref(c_result)})")
        status_code = poly_has_device(self.__communication_handle, c_device_type, c_device_number, byref(c_result))
        check_success("PolyHasDevice", status_code)

        return c_result.value

    def has_command(self, device_type, device_command, device_number=0):
        """
        Check if a device is available (e.g. sensor head nr. 0).

        Args:
            device_type:    The device type, e.g. Controller.
            device_number:  The device number, e.g. 0.
            device_command: The device command to be used for this operation (see device_command.py)

        Returns:
            True if available, false if not.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyHasCommand(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand, bool* result)
        poly_has_command = DeviceCommunication.device_communication_dll.PolyHasCommand

        poly_has_command.restype = c_int
        poly_has_command.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_bool)]

        # ctypes function parameter initialization
        c_device_type = c_int(device_type)
        c_device_number = c_int(device_number)
        c_device_command = c_int(device_command)
        c_result = c_bool()

        logging.debug(f"Library call: PolyHasCommand({self.__communication_handle}, {c_device_type}, "
                      f"{c_device_number}, {c_device_command}, {byref(c_result)})")
        status_code = poly_has_command(self.__communication_handle, c_device_type, c_device_number, c_device_command,
                                       byref(c_result))
        check_success("PolyHasCommand", status_code)

        return c_result.value


class UnableToLoadDllError(OSError):
    """Exception class raised when a dll could not be loaded"""
    pass


class DeviceNotConnectedError(ConnectionError):
    """Exception raised when trying to communicate with an invalid connection handle"""
    pass


class LibraryFunctionCallError(ConnectionError):
    """Exception raised during device communication"""

    def __init__(self, function_name, status_code):
        self.function_name = function_name
        self.status_code = status_code

    def __str__(self):
        return f"{self.function_name} failed --> [{self.status_code}] " \
            f"\"{DeviceCommunication.last_error()}\""
