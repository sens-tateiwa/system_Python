"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import logging
from ctypes import *

from polytec.io.device_communication import DeviceCommunication, DeviceNotConnectedError, check_success


class ChannelActivation:
    """
    The channel activation class handles channel activation commands.

    Enable and disable methods are only available for device that support the DaqActiveChannels command (e.g. VFX-F-110)

    """

    def __init__(self, device_communication):
        """
        Constructor

        Args:
            device_communication:   An active device communication instance
        """
        self.__device_communication = device_communication

    def max_channel_count(self, channel_type):
        """
        Get the maximum amount of channels supported on a device (available or not).

        See PolyChannelActivationIsChannelTypeSupported and PolyChannelActivationIsChannelAvailable for further
        information on supported and available channels.

        Args:
            channel_type:   The channel type.

        Returns:
            Number of channels supported.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationMaxChannelCount(int communicationHandle, int channelType, int* count)
        poly_channel_activation_max_channel_count = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationMaxChannelCount
        poly_channel_activation_max_channel_count.restype = c_int
        poly_channel_activation_max_channel_count.argtypes = [c_int, c_int, POINTER(c_int)]

        c_channel_type = c_int(channel_type)
        c_channel_count = c_int()

        logging.debug(f"Library call: PolyChannelActivationMaxChannelCount("
                      f"{self.__device_communication.communication_handle},"
                      f"{c_channel_type}, {byref(c_channel_count)})")
        status_code = poly_channel_activation_max_channel_count(self.__device_communication.communication_handle,
                                                                c_channel_type, byref(c_channel_count))
        check_success(f"PolyChannelActivationMaxChannelCount", status_code)

        return c_channel_count.value

    def is_channel_type_supported(self, channel_type):
        """
        Check if a channel type is supported by a device.

        Args:
            channel_type:   The channel type.

        Returns:
            The result, true if channel type is available.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationIsChannelTypeSupported(int communicationHandle, int channelType, bool* result)
        poly_channel_activation_is_channel_type_supported = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationIsChannelTypeSupported
        poly_channel_activation_is_channel_type_supported.restype = c_int
        poly_channel_activation_is_channel_type_supported.argtypes = [c_int, c_int, POINTER(c_bool)]

        c_channel_type = c_int(channel_type)
        c_is_supported = c_bool()

        logging.debug(f"Library call: PolyChannelActivationIsChannelTypeSupported("
                      f"{self.__device_communication.communication_handle}, "
                      f"{c_channel_type}, {byref(c_is_supported)})")
        status_code = poly_channel_activation_is_channel_type_supported(
            self.__device_communication.communication_handle, c_channel_type, byref(c_is_supported))
        check_success(f"PolyChannelActivationIsChannelTypeSupported", status_code)

        return c_is_supported.value

    def is_channel_available(self, channel_type, channel_id=0):
        """
        Check if a channel is currently available to be enabled on a device. Already enabled channels also return true.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.

        Returns:
            The result, true if channel is available.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationIsChannelAvailable(int communicationHandle, int channelType, int channelId,
        #                                             bool* result)
        poly_channel_activation_is_channel_available = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationIsChannelAvailable
        poly_channel_activation_is_channel_available.restype = c_int
        poly_channel_activation_is_channel_available.argtypes = [c_int, c_int, c_int, POINTER(c_bool)]

        c_channel_type = c_int(channel_type)
        c_channel_id = c_int(channel_id)
        c_is_available = c_bool()

        logging.debug(f"Library call: PolyChannelActivationIsChannelAvailable("
                      f"{self.__device_communication.communication_handle},"
                      f"{c_channel_type}, {c_channel_id}), {byref(c_is_available)})")
        status_code = poly_channel_activation_is_channel_available(self.__device_communication.communication_handle,
                                                                   c_channel_type, c_channel_id, byref(c_is_available))
        check_success(f"PolyChannelActivationIsChannelAvailable", status_code)

        return c_is_available.value

    def enable_channel(self, channel_type, channel_id=0):
        """
        Enable the specified channel.

        Not available on IVS-500 and VGO-200 devices.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationEnableChannel(int communicationHandle, int channelType, int channelId)
        poly_channel_activation_enable_channel = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationEnableChannel
        poly_channel_activation_enable_channel.restype = c_int
        poly_channel_activation_enable_channel.argtypes = [c_int, c_int, c_int]

        c_channel_type = c_int(channel_type)
        c_channel_id = c_int(channel_id)

        logging.debug(f"Library call: PolyChannelActivationEnableChannel("
                      f"{self.__device_communication.communication_handle}, {c_channel_type}, {c_channel_id})")
        status_code = poly_channel_activation_enable_channel(self.__device_communication.communication_handle,
                                                             c_channel_type, c_channel_id)
        check_success(f"PolyChannelActivationEnableChannel", status_code)

    def disable_channel(self, channel_type, channel_id=0):
        """
        Disable the specified channel.

        Not available on IVS-500 and VGO-200 devices.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationDisableChannel(int communicationHandle, int channelType, int channelId)
        poly_channel_activation_disable_channel = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationDisableChannel
        poly_channel_activation_disable_channel.restype = c_int
        poly_channel_activation_disable_channel.argtypes = [c_int, c_int, c_int]

        c_channel_type = c_int(channel_type)
        c_channel_id = c_int(channel_id)

        logging.debug(f"Library call: PolyChannelActivationDisableChannel("
                      f"{self.__device_communication.communication_handle},"
                      f"{c_channel_type}, {c_channel_id})")
        status_code = poly_channel_activation_disable_channel(self.__device_communication.communication_handle,
                                                              c_channel_type, c_channel_id)
        check_success(f"PolyChannelActivationDisableChannel", status_code)

    def disable_all_channels(self):
        """
        Disable all channels on the device.

        Not available on IVS-500 and VGO-200 devices.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationDisableAllChannels(int communicationHandle)
        poly_channel_activation_disable_all_channels = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationDisableAllChannels
        poly_channel_activation_disable_all_channels.restype = c_int
        poly_channel_activation_disable_all_channels.argtypes = [c_int]

        logging.debug(f"Library call: PolyChannelActivationDisableAllChannels("
                      f"{self.__device_communication.communication_handle}")
        status_code = poly_channel_activation_disable_all_channels(self.__device_communication.communication_handle)
        check_success(f"PolyChannelActivationDisableAllChannels", status_code)

    def is_channel_enabled(self, channel_type, channel_id=0):
        """
        Check if the specified channel is enabled.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.

        Returns:
            The result, true if channel is enabled.

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before starting to communicate with it.")

        # int PolyChannelActivationIsChannelEnabled(int communicationHandle, int channelType, int channelId,
        #                                           bool* result)
        poly_channel_activation_is_channel_enabled = \
            DeviceCommunication.device_communication_dll.PolyChannelActivationIsChannelEnabled
        poly_channel_activation_is_channel_enabled.restype = c_int
        poly_channel_activation_is_channel_enabled.argtypes = [c_int, c_int, c_int, POINTER(c_bool)]

        c_channel_type = c_int(channel_type)
        c_channel_id = c_int(channel_id)
        c_is_enabled = c_bool()

        logging.debug(f"Library call: PolyChannelActivationIsChannelEnabled("
                      f"{self.__device_communication.communication_handle},"
                      f"{c_channel_type}, {c_channel_id}, {byref(c_is_enabled)})")
        status_code = poly_channel_activation_is_channel_enabled(self.__device_communication.communication_handle,
                                                                 c_channel_type, c_channel_id, byref(c_is_enabled))
        check_success(f"PolyChannelActivationIsChannelEnabled", status_code)

        return c_is_enabled.value
