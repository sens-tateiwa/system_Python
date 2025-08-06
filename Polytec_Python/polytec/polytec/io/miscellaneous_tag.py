"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

from enum import IntEnum, unique


@unique
class MiscellaneousTag(IntEnum):
	"""Additional information for some [commands](\ref PTCDeviceCommand)."""

	"""
	Invalid default value.
	Use PTCMiscellaneousTag_None instead if the field is not used.
	"""
	Unknown = 0,

	"""Indicates that the PTCMiscellaneousTag is not used."""
	NoTag = 1,

	"""A channel with the index number 0."""
	Channel0 = 2,

	"""A channel with the index number 1."""
	Channel1 = 3,

	"""A channel with the index number 2."""
	Channel2 = 4,

	"""A channel with the index number 3."""
	Channel3 = 5,

	"""A channel with the index number 4."""
	Channel4 = 6,

	"""A channel with the index number 5."""
	Channel5 = 7,

	"""A channel with the index number 6."""
	Channel6 = 8,

	"""A channel with the index number 7."""
	Channel7 = 9,

	"""Channel X."""
	ChannelX = 10,

	"""Channel Y."""
	ChannelY = 11,

	"""
	Indicates that the command is applied to all devices of the given device type.
	The devices are treated as one device. The device number will be ignored.
	Typically used for decoder commands, e.g. to set all decoders to the same value at once.
	"""
	Combined = 12,

	"""AllChannels."""
	AllChannels = 13,

	"""Port number 0."""
	Port0 = 14,

	"""Port number 1."""
	Port1 = 15,

	"""A parameter with the index number 0."""
	Param0 = 16,

	"""A parameter with the index number 1."""
	Param1 = 17,

	"""A parameter with the index number 2."""
	Param2 = 18,

	"""A parameter with the index number 3."""
	Param3 = 19,

	"""A parameter with the index number 4."""
	Param4 = 20,

	"""A parameter with the index number 5."""
	Param5 = 21,

	"""A parameter with the index number 6."""
	Param6 = 22,

	"""A parameter with the index number 7."""
	Param7 = 23,

	"""Trigger channel"""
	ChannelTypeTrigger = 24,

	"""Velocity channel"""
	ChannelTypeVelocity = 25,

	"""Displacement channel"""
	ChannelTypeDisplacement = 26,

	"""Acceleration channel"""
	ChannelTypeAcceleration = 27,

	"""RSSI channel"""
	ChannelTypeRSSI = 28,

	"""Focus control board"""
	FocusControlBoard = 29,

	"""Default value"""
	DefaultValue = 30,

	"""Selected value"""
	SelectedValue = 31,

	"""Start up value"""
	StartUpValue = 32,

	"""Device index 0"""
	DeviceIndex0 = 33,

	"""Device index 1"""
	DeviceIndex1 = 34,

	"""Device index 2"""
	DeviceIndex2 = 35,

	"""Device index 3"""
	DeviceIndex3 = 36,

	"""Device index 4"""
	DeviceIndex4 = 37,

	"""Device index 5"""
	DeviceIndex5 = 38,

	"""Device index 6"""
	DeviceIndex6 = 39,

	"""Device index 7"""
	DeviceIndex7 = 40,

	"""Device index 8"""
	DeviceIndex8 = 41,

	"""Device index 9"""
	DeviceIndex9 = 42
