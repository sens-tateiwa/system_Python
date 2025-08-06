"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

from enum import IntEnum, unique


@unique
class ChannelType(IntEnum):
	"""Channel types of data acquisition channels"""

	"""Unknown channel type. Always an error if this occurs."""
	Unknown = 0,

	"""
	The data validity channel indicates if the data is valid. Invalid data may be caused by
	a lost UDP packet or a buffer overflow. (0 == invalid, 1 == valid).
	"""
	DataValidity = 1,

	"""The velocity channel contains the measured velocity."""
	Velocity = 2,

	"""The RSSI channel is a measure for the quality of the measurement data."""
	RSSI = 3,

	"""The trigger channel indicates if the trigger was pulled. (0 == trigger off, 1 == trigger on)."""
	Trigger = 4,

	"""The displacement channel contains the measured displacement."""
	Displacement = 6,

	"""The acceleration channel contains the measured acceleration."""
	Acceleration = 7
