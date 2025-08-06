"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import logging
from ctypes import *

from polytec.io.device_communication import DeviceCommunication, DeviceNotConnectedError, LibraryFunctionCallError
from polytec.io.device_communication import check_success
from polytec.io.communication_status_code import CommunicationStatusCode


class DataAcquisition:
    """Data Acquisition interface Python wrapper"""

    def __init__(self, device_communication, buffer_capacity):
        """
        Constructor

        Initializes the instance and opens a data acquisition communication with the device connected.

        Args:
            device_communication:   An active device communication instance to base the data acquisition on
            buffer_capacity:        The buffer capacity of the internal acquisition ring buffer in base samples

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        # initialize instance variables
        self.__acquisition_handle = None
        # open data acquisition
        self.__open_data_acquisition(device_communication, buffer_capacity)

    def __del__(self):
        """Destructor"""
        self.__close_data_acquisition()

    def __open_data_acquisition(self, device_communication, buffer_capacity):
        """
        Opens a data acquisition connection and allocates a ring buffer with the specified capacity for incoming data.

        Args:
            device_communication:   An active device communication instance to base the data acquisition on
            buffer_capacity:        The buffer capacity of the internal ring buffer in base samples

        Raises:
             DeviceNotConnectedError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if device_communication.communication_handle is None:
            raise DeviceNotConnectedError("You need to connect to a device before opening a data acquisition.")

        # int PolyOpenDataAcquisition(int* acquisitionHandle, int communicationHandle, size_t bufferCapacity)
        poly_open_data_acquisition = DeviceCommunication.device_communication_dll.PolyOpenDataAcquisition
        poly_open_data_acquisition.restype = c_int
        poly_open_data_acquisition.argtypes = [POINTER(c_int), c_int, c_long]

        # ctypes function parameter initialization
        self.__acquisition_handle = c_int()
        c_buffer_capacity = c_long(buffer_capacity)

        logging.debug(f"Library call: PolyOpenDataAcquisition"
                      f"({byref(self.__acquisition_handle)}, {device_communication.communication_handle}, "
                      f"{c_buffer_capacity})")
        status_code = poly_open_data_acquisition(byref(self.__acquisition_handle),
                                                 device_communication.communication_handle, c_buffer_capacity)

        if status_code != CommunicationStatusCode.Success:
            self.__acquisition_handle = None
            raise LibraryFunctionCallError("PolyOpenDataAcquisition", status_code)

    def __close_data_acquisition(self):
        """
        Closes a data acquisition connection.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is not None:
            # void PolyCloseDataAcquisition(int acquisitionHandle)
            poly_close_data_acquisition = DeviceCommunication.device_communication_dll.PolyCloseDataAcquisition
            poly_close_data_acquisition.argtypes = [c_int]

            logging.debug(f"Library call: PolyCloseDataAcquisition({self.__acquisition_handle})")
            poly_close_data_acquisition(self.__acquisition_handle)

    def __get_data(self, channel_type, channel_id, sample_count, poly_dll_get_data_function, return_type):
        """
        Gets the samples from the given channel.

        Args:
            channel_type:               The channel type.
            channel_id:                 The channel identifier.
            sample_count:               The amount of samples to get
            poly_dll_get_data_function: The DLL get data function to be used
            return_type:                The type of the data to be fetched copied from the internal buffers

        Returns:
            The data as a list of integers.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        c_data_arr = return_type * sample_count

        # int PolyGetUInt8Data(int acquisitionHandle, int channelType, int channelId, uint8_t* dataBuffer,
        #                      size_t bufferSize)
        poly_dll_get_data_function.restype = c_int
        poly_dll_get_data_function.argtypes = [c_int, c_int, c_int, POINTER(c_data_arr), c_long]

        # ctypes function parameter initialization

        c_channel_type = c_int(channel_type)
        c_channel_id = c_int(channel_id)
        c_data_buffer = c_data_arr()
        c_buffer_size = c_long(sample_count)

        logging.debug(f"Library call: PolyGet[{return_type.__name__}]Data({self.__acquisition_handle}, "
                      f"{c_channel_type}, {c_channel_id}, {byref(c_data_buffer)}, {c_buffer_size})")
        status_code = poly_dll_get_data_function(self.__acquisition_handle, c_channel_type, c_channel_id,
                                                 byref(c_data_buffer), c_buffer_size)
        check_success(f"PolyGet[{return_type.__name__}]Data", status_code)

        # convert ctype to python type
        return [c_data_buffer[i] for i in range(c_buffer_size.value)]

    def start_data_acquisition(self):
        """
        Starts acquiring data to the internal ring buffer.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyStartDataAcquisition(int acquisitionHandle)
        poly_start_data_acquisition = DeviceCommunication.device_communication_dll.PolyStartDataAcquisition
        poly_start_data_acquisition.restype = c_int
        poly_start_data_acquisition.argtypes = [c_int]

        logging.debug(f"Library call: PolyStartDataAcquisition({self.__acquisition_handle})")
        status_code = poly_start_data_acquisition(self.__acquisition_handle)
        check_success("PolyStartDataAcquisition", status_code)

    def stop_data_acquisition(self):
        """
        Stops acquiring data to the internal ring buffer.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyStopDataAcquisition(int acquisitionHandle)
        poly_stop_data_acquisition = DeviceCommunication.device_communication_dll.PolyStopDataAcquisition
        poly_stop_data_acquisition.restype = c_int
        poly_stop_data_acquisition.argtypes = [c_int]

        logging.debug(f"Library call: PolyStopDataAcquisition({self.__acquisition_handle})")
        status_code = poly_stop_data_acquisition(self.__acquisition_handle)
        check_success("PolyStopDataAcquisition", status_code)

    def next_data_acquisition_block(self):
        """
        This method has to be called after all data from one block has been read and before data from the next block is
        read. The use of this method is only needed if multiple block acquisition is activated
        (DaqBlockCount != 1).

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyNextDataAcquisitionBlock(int acquisitionHandle)
        poly_next_data_acquisition_block = DeviceCommunication.device_communication_dll.PolyNextDataAcquisitionBlock
        poly_next_data_acquisition_block.restype = c_int
        poly_next_data_acquisition_block.argtypes = [c_int]

        logging.debug(f"Library call: PolyNextDataAcquisitionBlock({self.__acquisition_handle})")
        status_code = poly_next_data_acquisition_block(self.__acquisition_handle)
        check_success("PolyNextDataAcquisitionBlock", status_code)

    def read_data(self, requested_samples, timeout_ms):
        """
        Reads data from the ring buffer of the data acquisition into the measurement data buffer from which the samples
        then can be extracted using the get_[type]_data() functions (e.g. get_int32_data()).
        If the requested samples are not available in the given time, the function unblocks and raises a
        LibraryFunctionCallError.

        If data is acquired in block mode (DaqMode is supported and is set to "Block"), the requested sample count may
        not exceed the number of remaining samples in the block.

        Args:
            requested_samples:  The number of requested base samples.
            timeout_ms:         The timeout in milliseconds.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyReadData(int acquisitionHandle, size_t requestedSamples, int timeoutInMilliseconds)
        poly_read_data = DeviceCommunication.device_communication_dll.PolyReadData
        poly_read_data.restype = c_int
        poly_read_data.argtypes = [c_int, c_long, c_int]

        c_requested_samples = c_long(requested_samples)
        c_timeout_ms = c_int(timeout_ms)

        logging.debug(f"Library call: PolyReadData({self.__acquisition_handle}, {c_requested_samples}, {c_timeout_ms})")
        status_code = poly_read_data(self.__acquisition_handle, c_requested_samples, c_timeout_ms)
        check_success("PolyReadData", status_code)

    def read_available_data(self, requested_samples):
        """
        Reads data from the ring buffer of the data acquisition into the measurement data buffer from which the samples
        then can be extracted using the get_[type]_data() functions (e.g. get_int32_data()).
        If the requested samples are not available, the function only reads the currently available samples.

        Args:
            requested_samples:  The number of requested base samples.

        Returns:
            The number of base samples which have actually been extracted.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyReadAvailableData(int acquisitionHandle, size_t requestedSamples, size_t* extractedSamples)
        poly_read_available_data = DeviceCommunication.device_communication_dll.PolyReadAvailableData
        poly_read_available_data.restype = c_int
        poly_read_available_data.argtypes = [c_int, c_long, POINTER(c_long)]

        c_requested_samples = c_long(requested_samples)
        c_extracted_samples = c_long()

        logging.debug(f"Library call: PolyReadAvailableData({self.__acquisition_handle}, {c_requested_samples},"
                      f"{byref(c_extracted_samples)})")
        status_code = poly_read_available_data(self.__acquisition_handle, c_requested_samples,
                                               byref(c_extracted_samples))
        check_success("PolyReadAvailableData", status_code)
        return c_extracted_samples.value

    def available_samples(self):
        """
        Get sample count available to be extracted from all channels.

        Returns:
            Number of base samples available.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyAvailableSamples(int acquisitionHandle, size_t requestedSamples, size_t* extractedSamples)
        poly_available_samples = DeviceCommunication.device_communication_dll.PolyAvailableSamples
        poly_available_samples.restype = c_int
        poly_available_samples.argtypes = [c_int, POINTER(c_long)]

        c_available_samples = c_long()

        logging.debug(f"Library call: PolyAvailableSamples({self.__acquisition_handle}, {byref(c_available_samples)})")
        status_code = poly_available_samples(self.__acquisition_handle, byref(c_available_samples))
        check_success("PolyAvailableSamples", status_code)
        return c_available_samples.value

    def extracted_sample_count(self, channel_type, channel_id):
        """
        Get sample count extracted / available to be copied from the specified channel.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.

        Returns:
            Number of samples available to be copied.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyExtractedSampleCount(int acquisitionHandle, int channelType, int channelId,
        #                              size_t* extractedSamples)
        poly_extracted_sample_count = DeviceCommunication.device_communication_dll.PolyExtractedSampleCount
        poly_extracted_sample_count.restype = c_int
        poly_extracted_sample_count.argtypes = [c_int, c_int, c_int, POINTER(c_long)]

        c_channel_type = c_int(channel_type)
        c_channel_id = c_int(channel_id)
        c_available_samples = c_long()

        logging.debug(f"Library call: PolyExtractedSampleCount({self.__acquisition_handle}, {c_channel_type}, "
                      f"{c_channel_id}, {byref(c_available_samples)})")
        status_code = poly_extracted_sample_count(self.__acquisition_handle, c_channel_type, c_channel_id,
                                                  byref(c_available_samples))
        check_success("PolyExtractedSampleCount", status_code)
        return c_available_samples.value

    def get_uint8_data(self, channel_type, channel_id, sample_count):
        """
        Gets the samples from the given channel as UInt8 data.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.
            sample_count:   The amount of samples to get

        Returns:
            The data as a list of integers.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        return self.__get_data(channel_type, channel_id, sample_count,
                               DeviceCommunication.device_communication_dll.PolyGetUInt8Data, c_uint8)

    def get_int16_data(self, channel_type, channel_id, sample_count):
        """
        Gets the samples from the given channel as Int16 data.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.
            sample_count:   The amount of samples to get

        Returns:
            The data as a list of integers.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        return self.__get_data(channel_type, channel_id, sample_count,
                               DeviceCommunication.device_communication_dll.PolyGetInt16Data, c_int16)

    def get_uint16_data(self, channel_type, channel_id, sample_count):
        """
        Gets the samples from the given channel as UInt16 data.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.
            sample_count:   The amount of samples to get

        Returns:
            The data as a list of integers.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        return self.__get_data(channel_type, channel_id, sample_count,
                               DeviceCommunication.device_communication_dll.PolyGetUInt16Data, c_uint16)

    def get_int32_data(self, channel_type, channel_id, sample_count):
        """
        Gets the samples from the given channel as UInt16 data.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.
            sample_count:   The amount of samples to get

        Returns:
            The data as a list of integers.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        return self.__get_data(channel_type, channel_id, sample_count,
                               DeviceCommunication.device_communication_dll.PolyGetInt32Data, c_int32)

    def get_overrange(self, channel_type, channel_id, sample_count):
        """
        Gets the samples from the given channel as UInt16 data.

        Args:
            channel_type:   The channel type.
            channel_id:     The channel identifier.
            sample_count:   The amount of samples to get

        Returns:
            The data as a list of integers.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        return self.__get_data(channel_type, channel_id, sample_count,
                               DeviceCommunication.device_communication_dll.PolyGetOverrange, c_uint8)

    def channel_min_value(self, channel_type):
        """
        Evaluates the regular minimum value for the channel type.

        Some channels have a head room. In this case the returned value is including the head room. For example if a
        velocity range of 2 m/s is selected and the head room for the digital velocity channel is 10%, the minimum value
        would indicate a velocity of -2.2 m/s.

        Args:
            channel_type:   The channel type.

        Returns:
            The minimum value.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyChannelMinValue(int acquisitionHandle, int channelType, int* minValue)
        poly_channel_min_value = DeviceCommunication.device_communication_dll.PolyChannelMinValue
        poly_channel_min_value.restype = c_int
        poly_channel_min_value.argtypes = [c_int, c_int, POINTER(c_int)]

        c_channel_type = c_int(channel_type)
        c_min_value = c_int()

        logging.debug(f"Library call: PolyChannelMinValue({self.__acquisition_handle}, {c_channel_type}, "
                      f"{byref(c_min_value)})")
        status_code = poly_channel_min_value(self.__acquisition_handle, c_channel_type, byref(c_min_value))
        check_success("PolyChannelMinValue", status_code)
        return c_min_value.value

    def channel_max_value(self, channel_type):
        """
        Evaluates the regular maximum value for the channel type.

        Some channels have a head room. In this case the returned value is including the head room. For example if a
        velocity range of 2 m/s is selected and the head room for the digital velocity channel is 10%, the minimum value
        would indicate a velocity of -2.2 m/s.

        Args:
            channel_type:   The channel type.

        Returns:
            The maximum value.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyChannelMaxValue(int acquisitionHandle, int channelType, int* maxValue)
        poly_channel_max_value = DeviceCommunication.device_communication_dll.PolyChannelMaxValue
        poly_channel_max_value.restype = c_int
        poly_channel_max_value.argtypes = [c_int, c_int, POINTER(c_int)]

        c_channel_type = c_int(channel_type)
        c_max_value = c_int()

        logging.debug(f"Library call: PolyChannelMaxValue({self.__acquisition_handle}, {c_channel_type}, "
                      f"{byref(c_max_value)})")
        status_code = poly_channel_max_value(self.__acquisition_handle, c_channel_type, byref(c_max_value))
        check_success("PolyChannelMaxValue", status_code)
        return c_max_value.value

    def base_sample_rate_in_hz(self):
        """
        Retrieve the base sample rate of a device.

        Returns:
            The base sample rate in Hz.

        Raises:
             DataAcquisitionNotOpenError, LibraryFunctionCallError
        """
        assert DeviceCommunication.device_communication_dll is not None

        if self.__acquisition_handle is None:
            raise DataAcquisitionNotOpenError("No data acquisition opened.")

        # int PolyBaseSampleRateInHz(int acquisitionHandle, double* baseSampleRate)
        poly_base_sample_rate_in_hz = DeviceCommunication.device_communication_dll.PolyBaseSampleRateInHz
        poly_base_sample_rate_in_hz.restype = c_int
        poly_base_sample_rate_in_hz.argtypes = [c_int, POINTER(c_double)]

        c_base_sample_rate = c_double()

        logging.debug(f"Library call: PolyBaseSampleRateInHz({self.__acquisition_handle}, {byref(c_base_sample_rate)})")
        status_code = poly_base_sample_rate_in_hz(self.__acquisition_handle, byref(c_base_sample_rate))
        check_success("PolyBaseSampleRateInHz", status_code)
        return c_base_sample_rate.value


class DataAcquisitionNotOpenError(ConnectionError):
    """Exception raised when trying to use a data acquisition command with an invalid acquisition handle"""
    pass
