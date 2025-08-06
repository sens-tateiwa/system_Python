"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import logging
from ctypes import *

from polytec.io.device_communication import DeviceCommunication, DeviceNotConnectedError, check_success


class ItemList:
    """
    The ItemList class models an item list command like Range

    Item list commands return a comma separated list ("2 m/s,1 m/s,...") for GetValueList, all available indices for
    GetDevInfo and the current index for Get/Set.
    """

    def __init__(self, device_communication, device_type, device_command):
        """
        Constructor

        Args:
            device_communication:   An active device communication instance
            device_type:            The logical device (see device_type.py)
            device_command:         The item list command to be used (see device_command.py)
        """
        # initialize instance variables
        self.__device_communication = device_communication
        self.__device_type = device_type
        self.__device_command = device_command

    def all_items(self, max_items_string_length=1000):
        """
        Get all items of an item list from the connected device via the device communication interface

        An item list models a command like Range, that returns a comma separated list ("2 m/s,1 m/s,...") for
        GetValueList, all available indices for GetDevInfo and reads/writes the current index for Get/Set commands.

        Args:
            max_items_string_length:    The maximum length of the string buffer for the items string
                                        received from the device

        Returns:
            All valid items (available and not). Use get_available_items or is_item_available to check out item
            availability.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyItemListGetAllItems(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                             char* buffer, size_t bufferSize)
        poly_item_list_get_all_items = DeviceCommunication.device_communication_dll.PolyItemListGetAllItems

        poly_item_list_get_all_items.restype = c_int
        poly_item_list_get_all_items.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_char), c_long]

        # ctypes function parameter initialization
        c_device_type = c_int(self.__device_type)
        c_device_number = c_int(0)
        c_device_command = c_int(self.__device_command)
        c_items_buffer = create_string_buffer(max_items_string_length)
        c_buffer_size = c_long(max_items_string_length)

        logging.debug(f"Library call: PolyItemListGetAllItems({self.__device_communication.communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {c_items_buffer}, {c_buffer_size})")
        status_code = poly_item_list_get_all_items(self.__device_communication.communication_handle, c_device_type,
                                                   c_device_number, c_device_command, c_items_buffer, c_buffer_size)
        check_success("PolyItemListGetAllItems", status_code)

        return c_items_buffer.value.decode().split(",")

    def available_items(self, max_items_string_length=1000):
        """
        Get all available items of an item list from the connected device via the device communication interface

        An item list models a command like Range, that returns a comma separated list ("2 m/s,1 m/s,...") for
        GetValueList, all available indices for GetDevInfo and reads/writes the current index for Get/Set commands.

        Args:
            max_items_string_length:    The maximum length of the string buffer for the items string
                                        received from the device

        Returns:
            All available items

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyItemListGetAvailableItems(int communicationHandle, int deviceType, int deviceNumber,
        #                                   int deviceCommand, char* buffer, size_t bufferSize)
        poly_item_list_get_available_items =\
            DeviceCommunication.device_communication_dll.PolyItemListGetAvailableItems

        poly_item_list_get_available_items.restype = c_int
        poly_item_list_get_available_items.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_char), c_long]

        # ctypes function parameter initialization
        c_device_type = c_int(self.__device_type)
        c_device_number = c_int(0)
        c_device_command = c_int(self.__device_command)
        c_items_buffer = create_string_buffer(max_items_string_length)
        c_buffer_size = c_long(max_items_string_length)

        logging.debug(f"Library call: PolyItemListGetAvailableItems("
                      f"{self.__device_communication.communication_handle}, {c_device_type}, {c_device_number}, "
                      f"{c_device_command}, {c_items_buffer}, {c_buffer_size})")
        status_code = poly_item_list_get_available_items(self.__device_communication.communication_handle,
                                                         c_device_type, c_device_number, c_device_command,
                                                         c_items_buffer, c_buffer_size)
        check_success("PolyItemListGetAvailableItems", status_code)

        return c_items_buffer.value.decode().split(",")

    def current_item(self, max_item_string_length=100):
        """
        Get the current item list item from the connected device via the device communication interface

        An item list models a command like Range, that returns a comma separated list ("2 m/s,1 m/s,...") for
        GetValueList, all available indices for GetDevInfo and reads/writes the current index for Get/Set commands.

        Args:
            max_item_string_length:     The maximum length of an item string (string buffer size)

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyItemListGetCurrentItem(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                                char* buffer, size_t bufferSize)
        poly_item_list_get_current_item = DeviceCommunication.device_communication_dll.PolyItemListGetCurrentItem

        poly_item_list_get_current_item.restype = c_int
        poly_item_list_get_current_item.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_char), c_long]

        # ctypes function parameter initialization
        c_device_type = c_int(self.__device_type)
        c_device_number = c_int(0)
        c_device_command = c_int(self.__device_command)
        c_item_buffer = create_string_buffer(max_item_string_length)
        c_buffer_size = c_long(max_item_string_length)

        logging.debug(f"Library call: PolyItemListGetCurrentItem({self.__device_communication.communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {c_item_buffer}, {c_buffer_size})")
        status_code = poly_item_list_get_current_item(self.__device_communication.communication_handle, c_device_type,
                                                      c_device_number, c_device_command, c_item_buffer, c_buffer_size)
        check_success("PolyItemListGetCurrentItem", status_code)

        return c_item_buffer.value.decode()

    def set_current_item(self, item):
        """
        Set the current item list item on the connected device via the device communication interface

        An item list models a command like Range, that returns a comma separated list ("2 m/s,1 m/s,...") for
        GetValueList, all available indices for GetDevInfo and reads/writes the current index for Get/Set commands.

        Args:
            item:   The item list item (string) to be set

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyItemListSetCurrentItem(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                                const char* item)
        poly_item_list_set_current_item = DeviceCommunication.device_communication_dll.PolyItemListSetCurrentItem

        poly_item_list_set_current_item.restype = c_int
        poly_item_list_set_current_item.argtypes = [c_int, c_int, c_int, c_int, c_char_p]

        # ctypes function parameter initialization
        c_device_type = c_int(self.__device_type)
        c_device_number = c_int(0)
        c_device_command = c_int(self.__device_command)
        c_value = c_char_p(item.encode('utf-8'))

        logging.debug(f"Library call: PolyItemListSetCurrentItem({self.__device_communication.communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {c_value})")
        status_code = poly_item_list_set_current_item(self.__device_communication.communication_handle, c_device_type,
                                                      c_device_number, c_device_command, c_value)
        check_success("PolyItemListSetCurrentItem", status_code)

    def is_item_available(self, item):
        """
        Test if an item list item is available on the connected device via the device communication interface

        An item list models a command like Range, that returns a comma separated list ("2 m/s,1 m/s,...") for
        GetValueList, all available indices for GetDevInfo and reads/writes the current index for Get/Set commands.

        Args:
            item:   The item list item (string) to be tested availability

        Returns:
            True if the item is available, false if not.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyItemListIsItemAvailable(int communicationHandle, int deviceType, int deviceNumber, int deviceCommand,
        #                                 const char* item, bool* result)
        poly_item_list_is_item_available = DeviceCommunication.device_communication_dll.PolyItemListIsItemAvailable

        poly_item_list_is_item_available.restype = c_int
        poly_item_list_is_item_available.argtypes = [c_int, c_int, c_int, c_int, c_char_p, POINTER(c_bool)]

        # ctypes function parameter initialization
        c_device_type = c_int(self.__device_type)
        c_device_number = c_int(0)
        c_device_command = c_int(self.__device_command)
        c_value = c_char_p(item.encode('utf-8'))
        c_result = c_bool()

        logging.debug(f"Library call: PolyItemListIsItemAvailable({self.__device_communication.communication_handle}, "
                      f"{c_device_type}, {c_device_number}, {c_device_command}, {c_value}, {byref(c_result)})")
        status_code = poly_item_list_is_item_available(self.__device_communication.communication_handle, c_device_type,
                                                       c_device_number, c_device_command, c_value, byref(c_result))
        check_success("PolyItemListIsItemAvailable", status_code)

        return c_result.value
