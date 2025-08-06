"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

from enum import IntEnum, unique


@unique
class DeviceType(IntEnum):
	"""Device type used to communicate with a logical device"""

	"""Not used"""
	Unknown = 0,

	"""Controller"""
	Controller = 1,

	"""Sensor head"""
	SensorHead = 2,

	"""Preamp"""
	Preamp = 3,

	"""Input board"""
	InputBoard = 4,

	"""Oscillator"""
	Oscillator = 5,

	"""Velocity decoder analog"""
	VelocityDecoderAnalog = 6,

	"""Velocity decoder digital"""
	VelocityDecoderDigital = 7,

	"""Displacement decoder analog"""
	DisplacementDecoderAnalog = 8,

	"""Displacement decoder digital"""
	DisplacementDecoderDigital = 9,

	"""Output board analog"""
	OutputBoardAnalog = 10,

	"""Output board digital"""
	OutputBoardDigital = 11,

	"""Interface"""
	Interface = 12,

	"""UserBoard"""
	UserBoard = 13,

	"""Revolution decoder"""
	RevolutionDecoder = 14,

	"""Ethernet switch"""
	EthernetSwitch = 15,

	"""ADC board (used for reference channels)"""
	AdcBoard = 16,

	"""DAC board (used for generator channels)"""
	DacBoard = 17,

	"""Signal processing"""
	SignalProcessing = 18,

	"""Currently not used"""
	Decoder = 19,

	"""Sonde"""
	Sonde = 20,

	"""Axis"""
	Axis = 21,

	"""Acceleration decoder digital"""
	AccelerationDecoderDigital = 22,

	"""ADC adjustment"""
	AdcHardwareLayer = 23,

	"""DAC adjustment"""
	DacHardwareLayer = 24,

	"""QTec module"""
	QTecModule = 25,

	"""Camera Trigger"""
	CameraTrigger = 26
