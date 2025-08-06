"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

from enum import IntEnum, unique


@unique
class CommunicationStatusCode(IntEnum):
	"""Status codes for the device communication."""

	"""Success status code."""
	Success = 0,

	"""
	Unknown device error: The device firmware encountered an unknown error. May be a
	device command was used in an inappropriate way.
	"""
	UnknownDeviceError = 1,

	"""
	Wrong command type: The device firmware received a wrong command type. Command
	types are Get, GetDevInfo, GetValueList, Set.
	"""
	WrongCommandType = 2,

	"""
	Wrong device type: The device firmware received a wrong device type. A command was sent to
	a device which cannot handle it.
	"""
	WrongDeviceType = 3,

	"""Wrong device number: The device firmware received a command to a device number which is not installed."""
	WrongDeviceNumber = 4,

	"""
	Wrong attribute: The device firmware received a wrong device command, i.e. the command is not supported
	by the firmware. Device commands are e.g. Autofocus, LaserOn...
	"""
	WrongAttribute = 5,

	"""Wrong payload type: The device firmware received a Set-command with a wrong payload type."""
	WrongPayloadType = 6,

	"""
	Wrong payload data: The device firmware received a command with wrong payload data, i.e. with a
	value which is out of range.
	"""
	WrongPayloadData = 7,

	"""Scan array buffer underrun."""
	ScanArrayBufferUnderrun = 8,

	"""Scan array buffer overrun."""
	ScanArrayBufferOverrun = 9,

	"""Wrong extra tag: The device firmware received a command with a wrong miscellaneous tag."""
	WrongExtraTag = 10,

	"""Not installed: The device firmware received a command to a device type which is not installed."""
	NotInstalled = 11,

	"""Wrong operation mode."""
	WrongOperationMode = 12,

	"""Memory overrun."""
	MemoryOverrun = 13,

	"""Device not ready."""
	DeviceNotReady = 14,

	"""Device not responding."""
	DeviceNotResponding = 15,

	"""Wrong I2C answer."""
	WrongI2CAnswer = 16,

	"""Wrong CRC result."""
	WrongCRCResult = 17,

	"""Laser disabled."""
	LaserDisabled = 18,

	"""Flash device mismatch."""
	FlashDeviceMismatch = 19,

	"""Flash write failed."""
	FlashWriteFailed = 20,

	"""Sensor limit reached."""
	SensorLimitReached = 21,

	"""Not enough memory."""
	NotEnoughMemory = 22,

	"""Content mismatch."""
	ContentMismatch = 23,

	"""Execution failed."""
	ExecutionFailed = 24,

	"""Write-Lock failed. A write lock is needed to perform set commands on this device."""
	WriteLockFailed = 25,

	"""No permission."""
	NoPermission = 26,

	"""Invalid configuration."""
	InvalidConfiguration = 27,

	"""Unknown software error: An unknown error occurred in the interface software."""
	UnknownError = 2000,

	"""Logic error."""
	LogicError = 2001,

	"""Invalid argument."""
	InvalidArgument = 2002,

	"""Range error."""
	RangeError = 2003,

	"""System error."""
	SystemError = 2004,

	"""Bad cast."""
	BadCast = 2005,

	"""Bad alloc: Failed to allocate memory storage."""
	BadAlloc = 2006,

	"""Buffer overflow."""
	BufferOverflow = 2007,

	"""
	Timeout: The device is not responding within the timeout. A command was sent to the device but
	it is not responding.
	"""
	Timeout = 2008,

	"""Invalid response format: The device sent a response with an invalid format."""
	InvalidResponseFormat = 2009,

	"""
	Received wrong payload type: The received payload type from a Get/GetDevInfo/GetValueList-command
	does not match the expected payload type.
	"""
	ReceivedWrongPayloadType = 2010,

	"""Runtime error."""
	RuntimeError = 2011
