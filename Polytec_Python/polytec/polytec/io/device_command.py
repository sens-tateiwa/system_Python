"""
@package io
"""

# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

from enum import IntEnum, unique


@unique
class DeviceCommand(IntEnum):
	"""Device commands used to communicate with a device"""

	"""Not used. Always an error if this appears."""
	Unknown = 0,

	"""
	Name of the device.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| e.g. "IVS-500 Vibrometer Controller"
	"""
	Name = 6,

	"""
	Range for velocity and displacement decoder.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current Range as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available ranges as indexes
	GetValueList				| String		| Lists all available ranges as strings
	"""
	Range = 10,

	"""
	Hour meter
	
	-	Power-on time.
	-	Switching power on/off counter.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| [Power-on time [s], Switching power on/off counter]
	"""
	HourMeter = 14,

	"""
	Decoder bandwidth.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current bandwidth as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available bandwidths as indexes
	GetValueList				| String		| Lists all available bandwidths as strings
	"""
	Bandwidth = 18,

	"""Tracking filter range."""
	TrackingFilterRange = 20,

	"""The measure mode of the decoder."""
	MeasureMode = 26,

	"""
	Lists all available devices of this front-end
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| Lists all available devices
	"""
	DeviceList = 32,

	"""
	A list of device command values, that are available for this specific device.
	
	This is a standard command that is supported from all devices.
	It is used to discover the caps of the device.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| e.g. [34,...]
	"""
	CommandList = 34,

	"""
	Firmware Version of the device.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| e.g. "1.0001"
	"""
	FirmwareVersion = 36,

	"""
	Sensor head focus position.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current focus position
	GetDevInfo, GetValueList	| Int16			| [minPosition, maxPosition] allowed values range
	"""
	FocusPosition = 38,

	"""
	Sensor head laser Off / On.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current laser status: 0 == off, 1 == on
	GetDevInfo, GetValueList	| Int16			| [off, on]
	"""
	LaserOn = 46,

	"""
	Sensor head auto focus status.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current auto focus status: 0 == Stop/Not running, 1 == Start/Running
	GetDevInfo, GetValueList	| Int16			| [0 == Stop, 1 == Start] allowed values
	"""
	Autofocus = 64,

	"""
	Sensor head laser signal level.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get								| Int16			| Current laser signal level
	GetDevInfo, GetValueList		| Int16			| [minValue, maxValue] allowed range
	"""
	SignalLevel = 66,

	"""
	Sensor head calibration date [dd.mm.yy]:
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| Sets the last service date. Only available in service mode.
	Get, GetDevInfo, GetValueList	| String		| Calibration date, e.g. "23.04.12"
	"""
	CalibrationDate = 74,

	"""
	Sensor head auto focus result. I.e. has the last auto focus run succeeded or not.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get								| Int16			| Result of the last auto focus run: 0 == Not found, 1 == Found
	GetDevInfo, GetValueList		| Int16			| [0 == Not found, 1 == Found] allowed results
	"""
	AutofocusResult = 76,

	"""
	Sensor head auto focus area. I.e. to limit the range to save focusing time.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current auto focus area: [lower limit, upper limit]
	GetDevInfo, GetValueList	| Int16			| [minValue, maxValue] allowed range
	"""
	AutofocusArea = 78,

	"""
	Data acquisition operation mode.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current mode as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available modes as indexes
	GetValueList				| String		| Lists all available modes as strings, e.g. "off, DAQ"
	"""
	OperationMode = 86,

	"""
	Data acquisition IP addresses according to the used ports.
	
	See also IPPortNumbers and IPPortAssignments.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| -				| not supported
	GetDevInfo, GetValueList	| String		| Lists all IP addresses (duplicates are possible).\n The results of the three commands: IPAddresses, IPPortNumbers, IPPortAssignments are coupled via their indexes.\n e.g.: IPAddresses == ["192.168.104.51, 192.168.104.51, 192.168.104.52"],\n IPPortNumbers == [60112, 60113, 60114],\n IPPortAssignments == ["DAQ, Info, Gen"]
	"""
	IPAddressList = 88,

	"""
	Data acquisition destination IP address.
	
	This is the (PC) ip address where the device should send the measured data to.
	The device firmware sets a default value.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| String		| Destination address for the DAQ-Data.
	GetDevInfo, GetValueList	| String		| min/max destination IP address range that can be used for the set command. [min, max], e.g. [192.168.104.00, 192.168.104.255]
	"""
	DestinationIPAddress = 90,

	"""
	Data acquisition port numbers.
	
	See IPAddresses and IPPortAssignments.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| -				| not supported
	GetDevInfo, GetValueList	| Int32			| Lists all data acquisition port numbers.\n e.g.: IPAddresses == ["192.168.104.51, 192.168.104.51, 192.168.104.52"],\n IPPortNumbers == [60112, 60113, 60114],\n IPPortAssignments == ["DAQ, Info, Gen"]
	"""
	IPPortNumberList = 96,

	"""
	Data acquisition port assignments.
	
	See IPAddresses and IPPortNumbers.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| -				| not supported
	GetDevInfo, GetValueList	| String		| Lists the usage of the port numbers.\n e.g.: IPAddresses == ["192.168.104.51, 192.168.104.51, 192.168.104.52"],\n IPPortNumbers == [60112, 60113, 60114],\n IPPortAssignments == ["DAQ, Info, Gen"]
	"""
	IPPortAssignmentList = 98,

	"""
	The device temperature [°C].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| Current temperature [°C]
	"""
	Temperature = 106,

	"""
	Resets the controller.
	</summary>
	<remarks>
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| 1 == resets the controller
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	Reset = 126,

	"""
	The status information of the controller
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| Sets the status information
	Get, GetDevInfo, GetValueList	| String		| Gets the available status information
	"""
	ControllerStatus = 128,

	"""
	Starts the ARM bootloader.
	</summary>
	<remarks>
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| 1 == starts the bootloader
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	Bootloader = 130,

	"""
	The Mac-Address of the front end. Used to identify the front end.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| String		| e.g. "00-19-99-8D-45-97" \n + Port number as Extra Tag [FrontEndMiscellaneousTag]: Port0
	GetDevInfo, GetValueList	| Int16			| Count of available MAC-Addresses: E.g.: 1 -> Port0
	"""
	MacAddress = 132,

	"""
	The number of available channels for this device.
	
	This is a standard command that is supported from many devices.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| e.g. [4]
	"""
	ChannelCount = 146,

	"""
	Range finder data to communicate with the PSV-500 disatance sensor
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Ascii			| data
	Get, GetDevInfo, GetValueList	| Ascii			| data
	"""
	RangeFinderData = 154,

	"""
	TriggerIn.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| Current state of TriggerIn.\n 0 == low, 1 == high
	GetDevInfo, GetValueList	| Int16			| [0,1] allowed Values
	"""
	TriggerIn = 158,

	"""
	Generator channel offset value
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| Sets the offset value \n + Channel number as extra tag
	Get, GetDevInfo, GetValueList	| Int16			| DAC-Steps = (offset [V] / channel range [V]) * 2^16 (==DAC-Range) (e.g. 0.001) \n + Channel number as extra tag
	"""
	ChannelOffset = 164,

	"""
	Generator channel gain factor for each channel range.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Float32		| Sets the gain factor \n + Channel number as extra tag
	Get, GetDevInfo, GetValueList	| Float32		| Each channel range has one gain factor,\n e.g. channel range: "10 V" -> channel range gain factor: 0.998, 1.001 \n + Channel number as extra tag
	"""
	ChannelGainFactor = 166,

	"""
	Sensor head focus progress.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Stops the current focus run.\n 0 == Stop
	Get							| Int16			| Current focus status:\n 0 == Not running, 1 == Running
	GetDevInfo, GetValueList	| Int16			| [0 == Stop/Not running, 1 == Running] allowed values
	"""
	FocusProgress = 174,

	"""
	Bypass to I2C-device for EEPROM access.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Byte			| Sends bytes to an I2C-device (I2C address, Data0, Data1, ...)
	Get							| Byte			| Gets bytes from I2C-devcie (I2C address, ByteNumHigh, ByteNumLow)
	GetDevInfo, GetValueList	| -				| not supported
	"""
	BypassToI2CDevice = 176,

	"""
	Laser hour meter
	
	-	Power-on time.
	-	Switching power on/off counter.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int32			| Set the Hour-Meter-Data from the Laser to the actual point of time ("1" has to be send). Only available in service mode.
	Get, GetDevInfo, GetValueList	| Int32			| [Power-on time [s], Switching power on/off counter]
	"""
	LaserHourMeter = 180,

	"""
	Last service date [dd.mm.yy]:
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| Sets the last service date. Should only be used with a service dongle.
	Get, GetDevInfo, GetValueList	| String		| Last service date, e.g. "23.04.12"
	"""
	LastServiceDate = 182,

	"""
	Next service date [dd.mm.yy]:
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| Sets the Next service date. Should only be used with a service dongle.
	Get, GetDevInfo, GetValueList	| String		| Next service date, e.g. "23.04.13"
	"""
	NextServiceDate = 184,

	"""
	The bragg cell temperature [°C].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| Current temperature [°C]
	"""
	BraggCellTemperature = 190,

	"""
	The mode of the analog sync out signal, as e.g. Off, Sync, 10 MHz.
	The command SyncDataRateDivider(812) specifies the rate of the mode "Sync",
	which can be customized by the user.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current sync out configuration as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available sync out configuration as indexes
	GetValueList				| String		| Lists all available sync out configurations as strings
	"""
	SyncOut = 206,

	"""
	The headroom for the analog velocity output.
	
	A head-room of e.g. 1.1 for a velocity channel and a velocity range of 2 m/s
	with a analog output range (command 234) of 4.4 volt indicates that
	4 volt corresponds to 2 m/s.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| Gets the head room, e.g. 1.1 for 10% head room
	"""
	HeadroomAnalogOut = 222,

	"""
	The headroom for the digital velocity channel.
	
	A head-room of e.g. 1.1 for a velocity channel of data type Int16 and a velocity
	range of 2 m/s indicates that the maximum value for an Int16 represents a velocity of 2.2 m/s.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| Gets the head room, e.g. 1.1 for 10% head room
	"""
	HeadroomDigitalOut = 224,

	"""
	Signal delay of the analog channel [ns].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Signal delay of the current selected decoder range / tracking filter etc.
	"""
	AnalogSignalDelay = 228,

	"""
	Signal delay of the digital channel [ns].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Signal delay of the current selected decoder range / tracking filter etc.
	"""
	DigitalSignalDelay = 230,

	"""
	Decoder output range [V].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float			| Output range value of the decoder, e.g. 5.0.
	"""
	RangeAnalogOut = 234,

	"""
	Decoder output impedance.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Ascii			| Impedance string of the decoder, e.g. "50 Ohm", "HighZ".
	"""
	ImpedanceAnalogOut = 236,

	"""
	Over temperature of the Bragg-cell
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| 0 == no over temperature, 1 == over temperature
	GetDevInfo, GetValueList	| Int16			| [0, 1] possible values
	"""
	OverTemperature = 244,

	"""
	Bootloader data
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Byte			| Writes the data
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	BootloaderData = 266,

	"""
	Checksum over complete EEPROM content
	
	Used to check the equality of the installed decoders in a 3D-System.
	Checksum is generated over the ident- and the FPGA-register-EEPROMs.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| checksum of EEPROM content
	"""
	EEPROMChecksum = 270,

	"""
	Sensor head focus step reference run
	
	The sensor head calibrates the focus motor steps. This command may take several seconds.
	Used e.g. if the command 'SeekFocusStepDeviation' evaluates a to high deviation.
	Note: When done, the sensor head does not return to the position where he is started from.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| 0 == Stop/Not running, 1 == Start/Running
	GetDevInfo, GetValueList	| Int16			| [0 == Stop, 1 == Start] allowed values
	"""
	FocusStepReference = 310,

	"""
	Sensor head pilot laser Off / On. E.g. PSV-IR.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current laser status: 0 == off, 1 == on
	GetDevInfo					| Int16			| [0, 1]
	GetValueList				| String		| [off, on]
	"""
	PilotLaserOn = 330,

	"""
	The nominal laser wavelength [nm].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| Nominal laser wavelength [nm]\n e.g. HeNe sensor head: 632.8
	"""
	LaserWavelength = 334,

	"""
	Pilot laser power (== laser dimmer) [power steps]. E.g. PSV-IR.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current pilot laser power
	GetDevInfo, GetValueList	| Int16			| [min == laser power off, max == brightest laser state] allowed value range
	"""
	PilotLaserPower = 342,

	"""
	The unique Id of the device, e.g. the CPU Id
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| Gets the Id, e.g. 2f003e000747333231363430
	"""
	UniqueId = 362,

	"""
	Access to an I2C device. Parameter: I2C-Bus-Nr, I2C-Adr, Sub-Module in Dez
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| E.g.: 1,9,4,1,0,370,0,1,1,160,0,0,0,1,21,6,2,$[..]$$. MsgType,CmdNum,Set,Device,DevNum,Attribute,PayloadType,ExtraTag,I2C-BusNr,I2CAdr,SubDevAdr,EE-AdrPtr Hi,Low,Data[]
	Get								| String		| E.g.: 1,9,3,1,0,370,0,1,1,160,0,0,0,600. MsgType,CmdNum,Get,Device,DevNum,Attribute,PayloadType,ExtraTag,I2C-BusNr,I2CAdr,SubDevAdr,EE-AdrPtr Hi,Low,MaxBytetoRead
	GetDevInfo, GetValueList		| -				| not supported
	"""
	AccessI2CEEPROM = 370,

	"""
	The firmware build number is a unique number identifying an ARM firmware build
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| Gets the firmware build number
	"""
	FirmwareBuildNumber = 528,

	"""
	Prepares an FPGA firmware update and erases the FPGA flash
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int32			| Sets the number of pages to be written by the FpgaUpdateData in the following form (1, numberOfPages).
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	PrepareFpgaUpdate = 534,

	"""
	Writes a page of 256 bytes to the FPGA in text form
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| A flash page is sent as comma separated byte array in the following form (pageNumber, byte0, byte1, ...), e.g. 0,56,234,128,0,12,...
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	FpgaUpdateData = 536,

	"""
	System match status
	
	E.g. A-CTR-110: If all connected Axes Types correspond to the expected Axes Types,
	the system is matched. If one or more of the connected Axes Types differ from the expected Type,
	the system is not matched.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| 0 == mismatch, 1 == match
	"""
	SystemMatchStatus = 546,

	"""
	Hash array
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Byte			| Sets the hash array
	Get, GetDevInfo, GetValueList	| Byte			| Gets the hash array bytes
	"""
	HashArray = 552,

	"""
	High pass filter range.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current high pass filter as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available high pass filters as indexes
	GetValueList				| String		| Lists all available high pass filters as strings, e.g. ["Off,13 Hz,104 Hz"]
	"""
	HighPass = 558,

	"""
	Enables to activate the super user mode
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int32			| Activates the super user mode by sending the secret
	Get							| Int32			| The current super user mode
	GetDevInfo, GetValueList	| Int32			| [0 = inactive, 1 = active] The available super user modes
	"""
	SuperUser = 560,

	"""
	Load user settings.
	
	\see PTCDeviceCommand_SaveUserSettings for further information about user settings.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Loads the desired user setting
	Get							| Int16			| Gets the current user setting as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the available user settings as indexes
	GetValueList				| String		| Lists all user settings as string
	"""
	LoadUserSettings = 566,

	"""
	Baud rate for serial communication.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current baud rate as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the available baud rates as indexes
	GetValueList				| String		| Lists all baud rates as string
	"""
	BaudRate = 568,

	"""
	Save user settings.
	
	User settings are user defined settings like bandwidth, ranges, filters, etc. that can be saved to a user profile
	using this command. Use \ref PTCDeviceCommand_LoadUserSettings to load the user settings from a user profile
	at any given time. Use \ref PTCDeviceCommand_PowerUpSettings to define which settings to load on power up.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Saves the current settings as the desired user settings
	Get							| -				| not supported
	GetDevInfo					| Int16			| [index1, index2,...] Gets the available user settings as indexes
	GetValueList				| String		| Gets the available user settings as string
	"""
	SaveUserSettings = 570,

	"""
	Overrange for a decoder range, e.g. a velocity overrange.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| Current overrange status. The overrange status is internally buffered since the last request.
	GetDevInfo, GetValueList	| Int16			| [0 == no overrange, 1 == overrange] possible values
	"""
	Overrange = 572,

	"""
	Filter Off / On.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current filter status: 0 == off, 1 == on
	GetDevInfo					| Int16			| [0, 1]
	GetValueList				| String		| [off, on]
	"""
	AseFilterOn = 574,

	"""
	ASE filter range.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Float32		| + Extra Tag enum value \n Current ASE filter parameter value
	Get, GetDevInfo				| Int16			| [16, 17,...] Lists the available Extra Tag enum values
	GetDevInfo					| Float32		| + Extra Tag enum value \n [minValue, maxValue] allowed range of the parameter\n e.g. [-1, 0.9999]
	GetValueList				| String		| Lists all available ASE filter parameters as strings\n ["RSSI_T, RSSI_S, RSSI_C"]
	"""
	AseFilterParameter = 576,

	"""
	The IP address of the controller.
	
	Polytec::IO::CommandType	| Payload type	| Extra tag	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| String		| None		| The current IP address, e.g. 192.168.104.150.
	Get, Set					| Int16			| Param0	| The search IP property\n [0,1] -> [Off,On]
	GetDevInfo, GetValueList	| String		| None		| Allowed IP address range that can be used for the set command.\n [min, max], e.g. [192.168.0.1, 192.168.255.254]
	"""
	DeviceIPAddress = 578,

	"""
	Laser supply Off/On
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Switches the laser supply
	Get							| Int16			| Current setting
	GetDevInfo, GetValueList	| Int16			| [0 == Off, 1 == On] possible values
	"""
	PowerSupplyOn = 582,

	"""
	Axis type
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| Not supported
	Get							| Int16			| Current axis type
	GetDevInfo					| Int16			| Lists the available axis types as indices
	GetValueList				| String		| Lists all axis types as strings
	"""
	AxisType = 584,

	"""
	Controller power supply [0 = Off, 1 = On]
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Sets the power supply
	Get							| Int16			| Gets the power supply
	GetDevInfo, GetValueList	| Int16			| Gets possible values [0, 1]
	"""
	ControllerSupply = 586,

	"""
	Power-up settings
	
	\see PTCDeviceCommand_SaveUserSettings
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Sets the power-up settings by index
	Get							| Int16			| Gets the current power-up settings by index
	GetDevInfo					| Int16			| Lists available power-up settings as indices
	GetValueList				| String		| Lists all power-up settings as strings
	"""
	PowerUpSettings = 588,

	"""
	Power-up focus position
	
	[-1 = autofocus on power-up]
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Sets the desired power-up focus position
	Get							| Int16			| Gets the current power-up focus position
	GetDevInfo, GetValueList	| Int16			| Gets power-up focus position range [min, max]
	"""
	PowerUpFocusPosition = 590,

	"""
	The protocol type of the data acquisition
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| Gets the used protocol type of the DAQ
	"""
	DAQProtocolType = 592,

	"""
	High pass filter range cutoff frequencies [Hz]
	
	This are the frequencies, the filter attenuates the input by 3 dB.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Float32		| Current HighPass filter range cutoff frequency of the selected HighPass filter range.
	GetDevInfo, GetValueList	| Float32		| [cutoff1, cutoff2,...] Lists all available HighPass filter range cutoff frequencies.
	"""
	HPFilterRangeCutoff = 594,

	"""
	High pass filter range passband frequencies [Hz]. This are the frequencies, the filter is designed for.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Float32		| Current HighPass filter range passband frequency of the selected HighPass filter range.
	GetDevInfo, GetValueList	| Float32		| [passband1, passband2,...] Lists all available HighPass filter range passband frequencies.
	"""
	HPFilterRangePassband = 596,

	"""
	The serial number of the device
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| Sets the serial number
	Get, GetDevInfo, GetValueList	| String		| Gets the serial number
	"""
	SerialNumber = 604,

	"""
	Manual focus lock. A sensor head may have physical focus controls,
	which can be enabled or disabled by this command.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int16			| Current lock state as index
	GetDevInfo						| Int16			| [index1, index2,...] Lists the current available lock states as indexes
	GetValueList					| String		| Lists all available lock states as strings, e.g. ["Locked,Unlocked"]
	"""
	ManualFocusLock = 646,

	"""
	The signal delay of the FM signal in nanoseconds
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| the signal delay in nanoseconds
	"""
	QTecSignalDelayOfFMSignal = 658,

	"""
	FPGA Register Write Access
	
	Remark: This command is intended to directly communicate with the hardware.
	The commands WriteFpgaModuleRegister and WriteFpgaSubmoduleRegister are
	higher level and communicate with the decoder driver. This provides the concept
	of modules and submodules and provides safe access by locking.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Writes one or multiple values at the given address [address, values, ...]
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	WriteFpgaRegister = 660,

	"""
	FPGA Register Read Access
	
	Remark: This command is intended to directly communicate with the hardware.
	The commands ReadFpgaModuleRegister and ReadFpgaSubmoduleRegister are
	higher level and communicate with the decoder driver. This provides the concept
	of modules and submodules and provides safe access by locking.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Sets the read pointer and size to read [read pointer, number of values to read]
	Get, GetDevInfo, GetValueList	| UInt32		| Reads the given size of values at the read pointer
	"""
	ReadFpgaRegister = 662,

	"""
	The user ID is a string that can be set by a client to identify a device.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| Saves the UserId (maximum length 15 characters)
	Get, GetDevInfo, GetValueList	| String		| Gets the saved user ID or "Not available"
	"""
	UserId = 664,

	"""
	Possibility to change the function of the trigger-in pin
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Sets the trigger-in mode
	Get							| Int16			| Gets the current setting
	GetDevInfo, GetValueList	| Int16			| Gets the available settings \n (0 - trigger in data acquisition, 1 - switch laser, 2 - start autofocus, 3 - displacement clear)
	
	This command corresponds to the command PTCDeviceCommand_TriggerIn.
	"""
	TriggerInMode = 668,

	"""
	Log file packing
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Starts the log file packing (1 == Start)
	Get							| Int16			| Current progress of log file packing \n 0 == Not running, 1 == Running
	GetDevInfo, GetValueList	| Int16			| [0 == Not running, 1 == Running/Start] allowed values
	"""
	PackLogFiles = 670,

	"""
	Specifies if the controller acts as a DHCP client (gets the Ethernet configuration from a server) or if the Ethernet configuration is set manually.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| DHCP client: 1 == on (off is not supported, set a static IP address to disable DHCP)
	Get							| Int16			| DHCP client: 0 == off, 1 == on
	GetDevInfo, GetValueList	| Int16			| [off, on]
	"""
	DHCPClient = 672,

	"""
	The signal level of the decoder (level meter).
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| Current decoder signal level
	GetDevInfo, GetValueList	| Int16			| [minValue, maxValue] allowed range
	"""
	DecoderSignalLevel = 676,

	"""
	Low pass filter range.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current LowPass filter range as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available LowPass filter ranges as indexes
	GetValueList				| String		| Lists all available LowPass filter ranges as strings, e.g. ["Off,100 kHz,20 kHz,5 kHz"]
	"""
	LowPass = 678,

	"""
	Low pass filter range cutoff frequencies [Hz]
	
	This are the frequencies the filter attenuates the input by 3 dB.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Float32		| Current LowPass filter range cutoff frequency of the selected LowPass filter range.
	GetDevInfo, GetValueList	| Float32		| [cutoff1, cutoff2,...] Lists all available LowPass filter range cutoff frequencies.
	"""
	LPFilterRangeCutoff = 680,

	"""
	Low pass filter range passband frequencies [Hz]
	
	This are the frequencies, the filter is designed for.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Float32		| Current LowPass filter range passband frequency of the selected LowPass filter range.
	GetDevInfo, GetValueList	| Float32		| [passband1, passband2,...] Lists all available LowPass filter range passband frequencies.
	"""
	LPFilterRangePassband = 682,

	"""
	Evaluates if the decoder (of the corresponding device) is available
	
	E.g. the acceleration decoder may be only available for specific bandwidths.
	If the decoder is not available, it will be reachable via the command set but
	the signal will be turned off.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| Current decoder availability\n 0 == Not available, 1 == Available
	GetDevInfo, GetValueList	| Int16			| [0 == Not available, 1 == Available] allowed values
	"""
	DecoderAvailable = 684,

	"""
	The maximum acceleration of the decoder.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| The maximum acceleration as string e.g. “100 g” or "10 m/s"
	"""
	MaximumAcceleration = 686,

	"""
	The optimum range of the decoder.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| The optimum range as string (e.g. “>= 100 mm/s”)
	"""
	OptimumRange = 688,

	"""
	The maximum velocity range of the decoder, i.e. the velocity DC range if a high pass filter is enabled.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current maximum velocity range as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available maximum velocity ranges as indexes
	GetValueList				| String		| Lists all available maximum velocity ranges as strings
	"""
	MaximumVelocityRange = 690,

	"""
	Decoder auto range status.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current auto range status:\n 0 == Stop/Not running, 1 == Start/Running
	GetDevInfo, GetValueList	| Int16			| [0 == Stop, 1 == Start] allowed values
	"""
	AutoRange = 692,

	"""
	Log files download
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Byte			| Gets the device log files as zip file
	"""
	LogFilesDownload = 694,

	"""
	Indicates the server type of the communication server.
	
	On a device may be running several kinds of servers. Either the usual device server or
	other servers like e.g. a progress server or a fallback server.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| [0 = unknown, 1 = device server, 2 = progress server, 3 = fallback server]
	"""
	ServerType = 696,

	"""
	The displacement decoder overrun mode.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current overrun mode as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available overrun modes as indexes
	GetValueList				| String		| Lists all available overrun modes as strings
	"""
	OverrunMode = 700,

	"""
	Write lock
	
	The write-lock enables a client to get access to all set-commands. Otherwise the client has only access
	to all get-commands and a few set-commands.
	If the exclusive lock is already given to another client, the set-command returns with the error code #25 "WriteLock failed".
	If the client requests the write-lock explicitly with the write-lock command (strongly recommended),
	the write-lock set-command will never fail but the get-command tells if acquiring the write-lock has succeeded.
	For backwards compatibility and easier handling for small software-tools or development activities
	(e.g. debugging), if the client doesn't specify a write-lock mode, the write-lock mode "Non-Exclusive"
	is applied automatically when the client sends a set-command.
	
	a)	General:
	-	Only one client can have any kind of write-lock (exclusive or non-exclusive) at the same time.
	-	The write-lock has a timeout, i.e. the client need to send continuously commands to the controller
	to keep his write-lock alive (see WriteLockTimeout).
	
	b)	Exclusive write-lock (read/write):
	-	If acquiring succeeded, the get-command returns "Exclusive", otherwise "ReadOnly".
	-	Setting the exclusive write-lock disables the non-exclusive write-lock of all clients.
	-	The exclusive write-lock can't be disabled from another client.
	-	Only one exclusive write-lock per front-end is possible.
	
	c)	Non-Exclusive write-lock (read/write):
	-	If acquiring succeeded, the get-command returns "NonExclusive", otherwise "ReadOnly".
	-	If a client acquires the exclusive write-lock, the non-exclusive write-lock of another client is
	immediately taken away (set to "ReadOnly"). This client will receive the error code #25 "WriteLock failed"
	for his next set-command.
	-	Multiple non-exclusive write-locks per front-end are possible.
	
	d)	ReadOnly (write-lock off):
	-	The client has access to all get-commands.
	-	The client has only access to a few set-commands (e.g. WriteLock, Displacement clear).
	Using any other set-command will lead to the error code #25 "WriteLock failed".
	-	Multiple readonly write-locks per front-end are possible.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| The current lock mode as index.
	GetDevInfo					| Int16			| All possible lock modes as zero-based indices.\n [index1, index2, index3]
	GetValueList				| String		| All possible lock modes as strings.\n ["ReadOnly", "Exclusive", "NonExclusive"]
	"""
	WriteLock = 702,

	"""
	Write lock timeout
	
	If the client has enabled the write-lock, he need to send commands to the controller within this time span.
	Otherwise the controller will disable the write-lock for this client and the client will receive an error
	if sending a set-command.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| The write-lock timeout [s].
	"""
	WriteLockTimeout = 704,

	"""
	Evaluates if a displacement clear is available
	
	A displacement clear may not be available, e.g. if a high pass range is set.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| Current displacement clear availability\n 0 == Not available, 1 == Available
	GetDevInfo, GetValueList	| Int16			| [0 == Not available, 1 == Available] allowed values
	"""
	DisplacementClearAvailable = 706,

	"""
	Resets the displacement decoder to the zero position.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| 1 == Clear
	Get, GetDevInfo, GetValueList	| Int16			| [1] allowed values
	"""
	DisplacementClear = 708,

	"""
	The currently selected firmware component of the compute module
	
	Further commands as e.g. FirmwareComponentHashValue will be applied to this component.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current firmware component as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available firmware components as indices
	GetValueList				| String		| Lists all available firmware components as strings
	"""
	SelectedFirmwareComponent = 710,

	"""
	The hash value of the currently selected firmware component
	
	Firmware components can be selected by the command SelectedFirmwareComponent.
	The hash value can be used to compare firmware components, e.g. for a field update.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Byte			| Gets the hash value of a component as byte sequence.
	"""
	FirmwareComponentHashValue = 712,

	"""
	Uploads and initiates a field update
	
	This is an asynchronous command. To check if the command is currently running, use field update in progress (command 728).
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Byte			| Sends the new firmware as binary data, e.g. an archive file, to the device and initiates an update
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	FieldUpdate = 714,

	"""
	The clock management, e.g. MLV-F-110 (ARM).
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| The current clock management option as index.
	GetDevInfo					| Int16			| [index1, index2,...] All available clock management options as indices.
	GetValueList				| String		| All available clock management options as strings.\n E.g. ["single", "master", "slave"]
	"""
	ClockManagement = 724,

	"""
	This property indicates if a field update (command 714) is in progress.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| [0 == Not running, 1 == Running]
	GetDevInfo, GetValueList	| Int16			| [0 == Not running, 1 == Running] allowed values
	"""
	FieldUpdateInProgress = 728,

	"""
	The field update component progress
	
	The field update component progress indicates the progress of the component that is
	currently installed. Some components may take several minutes to be installed, so
	it may be necessary to get the update progress. The overall progress can be read by
	the FieldUpdateOverallProgress command and information about the currently installed
	component can be get by FieldUpdateProgressInfo.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| -				| not supported
	Get							| Int16			| Gets the progress of the component that is currently updated
	GetDevInfo, GetValueList	| Int16			| Gets the range of possible progress values [ 0, max ]
	"""
	FieldUpdateComponentProgress = 730,

	"""
	The field update progress info
	
	The field update progress info describes the component that is currently installed
	by the field update. To get progress information use the commands FieldUpdateOverallProgress
	and FieldUpdateComponentProgress.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| Gets information about the component that is currently updated [Done,Failed,...]
	"""
	FieldUpdateProgressInfo = 732,

	"""
	The fan speed in percent
	
	[0 = Min, 100 = Max]
	
	Polytec::IO::CommandType	| Payload type	| Extra tag     | Payload value
	----------------------------|---------------|---------------|------------------
	Set							| Int16			| None          | Sets the fan speed in percent. If the value is out of range, it is clamped to the allowed range
	Get							| Int16			| None          | Gets the fan speed in percent
	GetDevInfo, GetValueList	| Int16			| None          | Gets the value range [0, 100]
	Get							| Int16			| DefaultValue  | Gets the default fan speed in percent, e.g. 40
	"""
	FanSpeed = 734,

	"""
	The temperature at which the software should issue a warning
	
	This command refers to the temperature of the command: PTCDeviceCommand_Temperature.
	Using the real threshold temperature instead of just a bool (e.g. OverTemp) has two advantages:
	- If an application already displays the current temperature (polling), it does not need to poll the OverTemp command additionally.
	- The application can display the threshold temperature in the GUI.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| The warning temperature threshold [°C]
	"""
	WarningTemperatureThreshold = 736,

	"""
	Relays a compute module field update, e.g. for PSV-500 this enables to send a field update via DMS to the front-end.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Byte			| Sends the new firmware via a relay server to the device
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	RelayFieldUpdate = 740,

	"""
	FPGA module register write access
	
	With this command only registers that belong to a module can be written. For submodule
	registers use the command WriteFpgaSubmoduleRegister.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Writes one or multiple values at the given address [register address, values, ...]\n Remark: The register address consists of the module address (first 16 bit) and the actual register address (last 16 bit)
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	WriteFpgaModuleRegister = 742,

	"""
	FPGA module register read access
	
	With this command only registers that belong to a module can be read. For submodule
	registers use the command ReadFpgaSubmoduleRegister.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Reads the number of values and caches them [register address]\n Remark: The register address consists of the module address (first 16 bit) and the actual register address (last 16 bit)
	Get, GetDevInfo, GetValueList	| UInt32		| Reads the values from cache
	"""
	ReadFpgaModuleRegister = 744,

	"""
	FPGA submodule register write access
	
	With this command only registers that belong to a submodule can be written. For module
	registers use the command WriteFpgaModuleRegister.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Writes one or multiple values at the given address [register address, submodule address, values, ...]\n Remark: The register address consists of the module address (first 16 bit) and the actual register address (last 16 bit)
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	WriteFpgaSubmoduleRegister = 746,

	"""
	FPGA submodule register read access
	
	With this command only registers that belong to a submodule can be read. For module
	registers use the command ReadFpgaModuleRegister.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Reads the number of values and caches them [register address, submodule address]\n Remark: The register address consists of the module address (first 16 bit) and the actual register address (last 16 bit)
	Get, GetDevInfo, GetValueList	| UInt32		| Reads the values from cache
	"""
	ReadFpgaSubmoduleRegister = 748,

	"""
	The displacement clear mode
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| The current displacement clear mode as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available displacement clear modes
	GetValueList				| String		| [Analog,Digital] Lists all available displacement clear modes
	"""
	DisplacementClearMode = 750,

	"""
	FPGA module status register read access
	
	With this command only status registers that belong to a module can be read. For submodule
	status registers use the command ReadFpgaModuleStatusRegister.
	Each module has 16 status registers, which contain e.g. the date code.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Reads a status register value and caches it [module address, status register address]
	Get, GetDevInfo, GetValueList	| UInt32		| Reads the values from cache
	"""
	ReadFpgaModuleStatusRegister = 758,

	"""
	FPGA submodule status register read access
	
	With this command only status registers that belong to a submodule can be read. For module
	status registers use the command ReadFpgaModuleStatusRegister.
	Each submodule has 16 status registers, which contain e.g. the date code.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| UInt32		| Reads a status register value and caches it [module address, submodule address, status register address]
	Get, GetDevInfo, GetValueList	| UInt32		| Reads the values from cache
	"""
	ReadFpgaSubmoduleStatusRegister = 760,

	"""
	The IP address and subnet mask of the controller.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| String		| The current IP address and subnet mask\n e.g. 192.168.104.150, 255.255.255.0
	GetDevInfo, GetValueList	| -				| not supported
	"""
	DeviceIPAddressWithSubnetMask = 762,

	"""
	The hardware revision (16 bytes)
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Hex			| Sets the hardware revision (super user required)
	Get, GetDevInfo, GetValueList	| Hex			| Gets the hardware revision
	"""
	HardwareRevision = 764,

	"""
	The network hostname of the device
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| The hostname
	"""
	Hostname = 766,

	"""
	The stimuli generator may be used for gain-factor and offset adjustment
	
	It generates a signal for all outputs.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| The current stimuli generator signal as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the current available stimuli generator signals
	GetValueList				| String		| [Analog,Digital] Lists all available stimuli generator signals
	"""
	StimuliGenerator = 770,

	"""
	Indicates if the device runs in development mode, i.e. some parts may be simulated
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| 0 = production mode, 1 = development mode
	"""
	DevelopmentMode = 772,

	"""
	The demo mode expiration date, this command is optional.
	
	It may not be available if the license is without demo mode.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| demo mode expiration date, e.g. 31.12.18
	"""
	DemoModeExpirationDate = 776,

	"""
	The license validity.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| 0 = invalid license, 1 = valid license
	"""
	LicenseValidity = 778,

	"""
	The LVDS pre-emphases modes are different filters for the LVDS signal and may be used for different cable lengths
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| The current pre-emphases modes as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the currently available pre-emphases modes
	GetValueList				| String		| e.g. [Off,Low,Medium,High] Lists all available pre-emphases modes
	"""
	LVDSPreEmphasesModes = 784,

	"""
	The LVDS power off modes for switching the digital LVDS interface on or off
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| The current LVDS power off modes as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists the currently available LVDS power off modes
	GetValueList				| String		| e.g. [On,Off] Lists all available LVDS power off modes
	"""
	LVDSPowerOffModes = 786,

	"""
	Writes a page of 256 bytes to the FPGA as binary data
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Byte			| A flash page is sent in the following form (pageNumber, byte0, byte1, ...), where pageNumber is an Int32
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	FpgaUpdateByteData = 788,

	"""
	Activates the RSSI output
	
	This may be useful for adjustment if the decoder is not licensed.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| 1 = activate
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	ActivateRSSIOutput = 790,

	"""
	Output state of a device
	
	E.g. a hardware output may support velocity, displacement or acceleration signal. This
	command enables to switch between them by calling this command on a given decoder device.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Set							| Int16			| Activates the output (deactivating is not supported) and deactivates all others
	Get							| Int16			| Current output state 0 == Inactive, 1 == Active
	GetDevInfo, GetValueList	| Int16			| [0 == Inactive, 1 == Active] allowed values
	"""
	OutputActive = 796,

	"""
	Enable the display
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current display status: 0 == off, 1 == on
	GetDevInfo, GetValueList	| Int16			| [off, on]
	"""
	EnableDisplay = 802,

	"""
	Signal delay of the analog RSSI signal [ns].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Current signal delay of the RSSI signal
	"""
	AnalogRSSIDelay = 804,

	"""
	The FPGA temperature [°C].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| Current temperature [°C]
	"""
	FPGATemperature = 806,

	"""
	The temperature at which the software should issue a warning
	
	This command refers to the temperature of the command: PTCDeviceCommand_FPGATemperature.
	Using the real threshold temperature instead of just a bool (e.g. OverTemp) has two advantages:
	- If an application already displays the current temperature (polling), it does not need to poll the OverTemp command additionally.
	- The application can display the threshold temperature in the GUI.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| The warning temperature threshold [°C]
	"""
	WarningFPGATemperatureThreshold = 808,

	"""
	Indicates that a sensor head update will take place
	
	If "prepare update" has been sent, the FieldUpdateInProgress (728) command
	will show that an update is in progress, so that clients (e.g. an UI) may
	prepare for the update.
	If "start update" has been sent, the controller will reject all further
	commands that are not needed for the update.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| 1 == prepare update, 2 == start update
	Get, GetDevInfo, GetValueList	| Int16			| [1, 2] allowed values
	"""
	SensorHeadUpdateInProgress = 810,

	"""
	Sync data rate divider. This command facilitates to specify a divider rate of
	the sample rate for the sync output. If a divider of e.g. 2 is selected
	the analog sync out signal runs with half of the sample rate
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current sync data rate divider
	GetDevInfo, GetValueList	| Int16			| Allowed range [min, max]
	"""
	SyncDataRateDivider = 812,

	"""
	Fallback Power-up wavelength if no sensor head is connected
	
	The current wavelength can be retrieved by querying the Controller
	with the command LaserWavelength (334).
	This command enables to calibrate the system without
	sensor head.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Gets/Sets the current fallback power-up wavelength by index
	GetDevInfo					| Int16			| Lists available fallback power-up wavelength as indices
	GetValueList				| String		| [632.80 nm,1550.12 nm] Lists all power-up settings as strings
	"""
	FallbackPowerUpWavelength = 814,

	"""
	Package version of the device
	
	The package version describes the overall version of several firmware components
	like ARM firmware, FPGA image, compute module Software, ...
	If the package has no consistent package version because some components have been updated
	separately, the version "0.0.0.0" is returned.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| e.g. "1.0.19193.62374" for a consistent package
	"""
	PackageVersion = 816,

	"""
	Enable the wlan access point
	
	Setting this command can take a few seconds to complete (usually 1-3s). Set your communication timeout appropriately.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current access point status: 0 == off, 1 == on
	GetDevInfo, GetValueList	| Int16			| [off, on]
	"""
	AccessPoint = 828,

	"""
	WLAN access point user security key
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| String		| The security key to be set
	Get, GetDevInfo, GetValueList	| String		| The current security key
	"""
	AccessPointPassword = 830,

	"""
	WLAN access point SSID
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| Current SSID (e.g. "Polytec-VGO200-42")
	"""
	AccessPointSSID = 832,

	"""
	WiFi adapter status
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, GetDevInfo, GetValueList	| Int16			| Current WiFi adapter status: 0 == N/A, 1 == available, 2 == HW not supported, 3 == System rqmts. unsatisfied, 4 == Pending
	Set								| -				| not supported
	"""
	WifiAdapterStatus = 834,

	"""
	System display orientation
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Display orientation: 0 -> 0°, 1 -> 90°, 2 -> 180°, 3 -> 270° (counterclockwise)
	GetDevInfo, GetValueList	| Int16			| [0, 1, 2, 3]
	"""
	DisplayOrientation = 836,

	"""
	License file content.
	
	For TCP communcation only, since it may be larger than UDP packet size.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| gets the license file content
	"""
	LicenseFileContent = 838,

	"""
	The version info provides information about installed components of the system (e.g. ARM, FPGA, config files ...)
	
	For TCP communcation only, since it may be larger than UDP packet size.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| gets the version info
	"""
	VersionInfo = 840,

	"""
	QTec Off / On.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current QTec status: 0 == off, 1 == on
	GetDevInfo, GetValueList	| Int16			| [off, on]
	"""
	QTecOn = 862,

	"""
	The log level of compute module log files. This setting is stored, i.e. unchanged after restart.
	
	If the log level is set to Trace or Debug the device will show a warning that it is in development mode (see command 772).
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int16			| Current log level by index
	GetDevInfo						| Int16			| Lists available log levels as indices
	GetValueList					| String		| [Trace,Debug,Info,Warning,Error,Fatal] Lists all log levels as strings
	"""
	LogLevel = 916,

	"""
	Data acquisition sample rate in samples/s.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Gets the current sample rate
	"""
	DaqSampleRate = 918,

	"""
	Data acquisition mode. Differentiates between continuous streaming or blockwise acquisition.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int16			| Current data acquisition mode by index
	GetDevInfo						| Int16			| Lists data acquisition modes as indices
	GetValueList					| String		| [Streaming,Block] Lists all data acquisition modes as strings
	"""
	DaqMode = 920,

	"""
	Size of a data acquisition block in base sample rate, used in block mode.
	
	Has no effect on streaming mode.
	
	Range is affected by active channels & sample rate. Value will be clamped to the respective bounds
	if either active channels or sample rate are modified.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int32			| Current block size
	GetDevInfo, GetValueList	| Int32			| Allowed range [min, max]
	"""
	DaqBlockSize = 922,

	"""
	Amount of blocks to acquire during block mode.
	
	Setting this Value to 0 enables endless block transmission.
	Has no effect on streaming mode.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int16			| Current block Count
	GetDevInfo, GetValueList		| Int16			| Allowed range [min, max]
	"""
	DaqBlockCount = 924,

	"""
	Data acquisition trigger mode.
	
	Has no effect on streaming mode.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int16			| Current trigger mode by index
	GetDevInfo						| Int16			| Lists trigger modes as indices
	GetValueList					| String		| [None,Extern,Intern,Analog] Lists all trigger modes as strings
	"""
	DaqTriggerMode = 926,

	"""
	Data acquisition trigger edge.
	
	Has no effect on streaming mode.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int16			| Current trigger edge by index
	GetDevInfo						| Int16			| Lists trigger edges as indices
	GetValueList					| String		| [Falling,Rising] Lists all trigger edges as strings
	"""
	DaqTriggerEdge = 928,

	"""
	Gated trigger. Enabling this setting will use the external trigger signal as a gate for the internal or analog trigger.
	Triggering is only possible if the gate-signal (external trigger signal) is 1.
	
	Only has an effect when using the internal or analog trigger. Has no effect on streaming mode.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current gated trigger setting: 0 == off, 1 == on
	GetDevInfo, GetValueList	| Int16			| [off, on]
	"""
	DaqGatedTrigger = 930,

	"""
	Data acquisition pre/post trigger in signal samples (measurement sample rate).
	
	Has no effect on streaming mode.
	
	Range is affected by active channels & sample rate. Value will be clamped to the respective bounds
	if either active channels or sample rate are modified.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Int32			| Pre/Post trigger size in signal samples (positive value --> pre trigger, negative value --> post trigger)
	GetDevInfo, GetValueList		| Int32			| Allowed range [min, max]
	"""
	DaqPreTrigger = 932,

	"""
	Data acquisition analog trigger level.
	
	Only takes effect in analog triggered block mode.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Float32		| Trigger level for the analog trigger as a factor of the maximum amplitude
	GetDevInfo, GetValueList		| Float32		| Allowed range [min, max]
	"""
	DaqAnalogTriggerLevel = 934,

	"""
	Signal delay of the digital RSSI signal [ns].
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Current signal delay of the RSSI signal
	"""
	DigitalRSSIDelay = 936,

	"""
	Unloaded modules are features that are licensed but could not be loaded, due to missing components,
	e.g. a missing data acquisition driver or a missing hardware board.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| String		| Unloaded modules as comma separeted list, e.g. "Digital Data Acquisition,LVDS"
	"""
	UnloadedModules = 938,

	"""
	Strech factor for QTec filter (e.g. for FIR-64)
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int32			| sets the strech factor
	Get, GetDevInfo, GetValueList	| Int32			| gets the strech factor
	"""
	QTecFilterStretchFactor = 940,

	"""
	FPGA version of the device.
	
	Format:
	AA,B,CC,DD,EE,FF,GG,H
	
	AA = MODULE_ID = DEVTYPE_DMB = 25
	B = MAJOR(0... 9)
	CC = MINOR(00... 99)
	DD = CHANGE(00... 99)
	EE = YEAR(20... 99)
	FF = MONTH(01... 12)
	GG = MDAY(01... 31)
	H = DREV(“A”, “B”, “C”, ...)
	
	Polytec::IO::CommandType		| Payload type	| Extra tag				|Payload value
	--------------------------------|---------------|-----------------------|------------------------
	Set								| -				| -						| not supported
	Get, GetDevInfo, GetValueList	| String		| None, DeviceIndex0	| FPGA version of default FPGA
	Get, GetDevInfo, GetValueList	| String		| DeviceIndex1			| FPGA version of lattice FPGA
	"""
	FpgaVersion = 958,

	"""
	The test mode of digital data acquisition, e.g. for saw tooth or performance tests.
	If disabled ("Off") the output provides the actual measurement signal.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current measure mode as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists all available measure modes as indexes
	GetValueList				| String		| Lists all available measure modes as strings, e.g. "Off", "SawTooth", "Performance"
	"""
	DaqTestMode = 976,

	"""
	Active data acquisition channels
	
	The payload [-1] is used to indicate an empty list.
	
	Polytec::IO::CommandType		| Payload type	| Extra tag		| Payload value
	--------------------------------|---------------|---------------|-----------------
	Get, Set						| Int16			| ChannelType	| Active channels as list, e.g. [-1] -> all channels off, [0] -> top channel active, [0,1,2] -> top, left, right channels active
	GetDevInfo						| Int16			| ChannelType	| Current possible number of active channels, e.g. 1 (due to limited bandwidth, including active channels)
	GetValueList					| Int16			| ChannelType	| Maximum possible number of active channels, e.g. 3
	Get, GetDevInfo, GetValueList	| Int16			| None			| List of available channel types as extra tag, e.g. [Velocity,RSSI,Trigger]
	Set								| -				| None			| not supported
	"""
	DaqActiveChannels = 978,

	"""
	The result of data acquisition tests, e.g. of DaqTestMode performance test
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Float32		| test result
	"""
	DaqTestResult = 980,

	"""
	Maximum length of data acquisition output packets in base samples.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Reads the max. amount of base samples contained in a DAQ output packet
	"""
	DaqMaxPacketLengthInBaseSamples = 982,

	"""
	Size of a single data acquisition base sample in bytes.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Reads the size of a single base sample in bytes
	"""
	DaqBaseSampleSizeInBytes = 984,

	"""
	Data acquisition base sample rate.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Reads the data acquisition base sample rate
	"""
	DaqBaseSampleRate = 986,

	"""
	Data acquisition measurement number of the measurement currently being configured.
	This number will be used in the header of the data acquisition network packets for the next measurement.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| Reads the measurement number
	"""
	DaqMeasurementNumber = 988,

	"""
	The data acquisition trigger source channel type.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current trigger source as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists all available trigger sources
	GetValueList				| String		| Lists all available trigger sources as strings, e.g. "Velocity", "Displacement", "Acceleration"
	"""
	DaqAnalogTriggerSource = 990,

	"""
	The QTec interface version may be used to determine which
	filter coefficients need to be written to the QTec module.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| the interface version
	"""
	QTecInterfaceVersion = 994,

	"""
	The LVDS signal "A". LVDS signals enable a digital data acquisition in real time.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current LVDS signal as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists all available current LVDS signals
	GetValueList				| String		| Lists all available LVDS signals as strings, e.g. "Velocity", "Displacement", "Acceleration", "RSSI"
	"""
	LVDSSignalA = 996,

	"""
	The LVDS signal "B". LVDS signals enable a digital data acquisition in real time.
	
	Polytec::IO::CommandType	| Payload type	| Payload value
	----------------------------|---------------|------------------
	Get, Set					| Int16			| Current LVDS signal as index
	GetDevInfo					| Int16			| [index1, index2,...] Lists all available current LVDS signals
	GetValueList				| String		| Lists all available LVDS signals as strings, e.g. "Velocity", "Displacement", "Acceleration", "RSSI"
	"""
	LVDSSignalB = 998,

	"""Start bootloader for target"""
	BootloaderStartForTarget = 1000,

	"""Read / write bootloader flash"""
	BootloaderReadWriteFlash = 1002,

	"""Bootloader command"""
	BootloaderCommand = 1004,

	"""Erase bootloader application flash"""
	BootloaderEraseApplicationFlash = 1006,

	"""Gets the application start address of the given target"""
	BootloaderApplicationStartAddress = 1008,

	"""Start application"""
	BootloaderStartApplication = 1010,

	"""Start DMB application"""
	BootloaderStartDMBApplication = 1014,

	"""
	Checks if the bootloader or application is running
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int16			| if bootloader is running (0 = application is running, 1 = bootloader is running)
	"""
	BootloaderRunning = 1016,

	"""
	Data acquisition analog trigger hysteresis offset.
	
	The value of the analog trigger signal (see PTCDeviceCommand_DaqAnalogTriggerSource) has to surpass
	the trigger value plus/minus this hysteresis offset, depending on falling/rising edge (see PTCDeviceCommand_DaqTriggerEdge),
	before the analog trigger can take effect (falling -> plus, rising -> minus).
	This is used to avoid accidental triggers caused through noisy signals.
	
	Example:
	-	AnalogTriggerValue = 0.1
	-	AnalogTriggerHysteresisOffset = 0.02
	-	TriggerEdge = Rising
	-->	The signal level needs to dip below 0.08 (0.1 - 0.02) before a signal above 0.1 can fire the trigger
	
	Only takes effect in analog triggered block mode.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Get, Set						| Float32		| Trigger hysteresis for the analog trigger as a factor of the maximum amplitude
	GetDevInfo, GetValueList		| Float32		| Allowed range [min, max]
	"""
	DaqAnalogTriggerHysteresisOffset = 1054,

	"""
	List of status messages to be displayed as device status log on a client application, e.g. device UI, VibSoft.
	
	The element -1 is always present and indicates no message (it exists to always provide valid values for GetDevInfo and GetValueList).
	
	Polytec::IO::CommandType		| Payload type	| Parameter type	| Payload value
	--------------------------------|---------------|-------------------|------------------
	GetDevInfo, GetValueList		| Int32			| Void				| The range of available list elements [-1, N]
	Get								| String		| Int32				| The status message for a given list element: (index) -> "Error: message" or "Warning: message"
	Set								| -				| -					| not supported
	"""
	StatusMessages = 1056,

	"""
	The IQ mode facilitates to output the raw signal of the base band without demodulation.
	
	To change the IQ mode a system restart is required.
	
	Polytec::IO::CommandType	| Payload type	| Extra tag		| Payload value
	----------------------------|---------------|---------------|------------------
	Get, Set					| Int16			| None			| Current IQ mode as index (active at restart)
	GetDevInfo					| Int16			| None			| [index1, index2,...] Lists all available current IQ modes
	GetValueList				| String		| None			| Lists all available IQ modes as strings: [Off, On]
	Get							| Int16			| StartUpValue	| Active IQ mode as index for this start up session
	"""
	IQMode = 1058,

	"""
	Control publicly available decoder values.
	
	Caution! SelectedValue payload is provided as raw bytes and may contain data of any 32bit type (e.g. signed or float).
	Make sure to interpret the payload as the correct type.
	
	Polytec::IO::CommandType		| Payload type	| Extra tag		| Payload value
	--------------------------------|---------------|---------------|------------------
	Set								| String		| None			| Set currently selected decoder definition
	Get, GetDevInfo, GetValueList	| String		| None			| Get currently selected decoder definition
	Set								| UInt32		| SelectedValue	| Set the selected decoder definition value
	Get, GetDevInfo, GetValueList	| UInt32		| SelectedValue	| Get the selected decoder definition value
	"""
	DecoderValues = 1060,

	"""
	Control protected decoder values.
	
	You need to have super user rights to use this command (see SuperUser command).
	
	Caution! SelectedValue payload is provided as raw bytes and may contain data of any 32bit type (e.g. signed or float).
	Make sure to interpret the payload as the correct type.
	
	Polytec::IO::CommandType		| Payload type	| Extra tag		| Payload value
	--------------------------------|---------------|---------------|------------------
	Set								| String		| None			| Set currently selected decoder definition
	Get, GetDevInfo, GetValueList	| String		| None			| Get currently selected decoder definition
	Set								| UInt32		| SelectedValue	| Set the selected decoder definition value
	Get, GetDevInfo, GetValueList	| UInt32		| SelectedValue	| Get the selected decoder definition value
	"""
	ProtectedDecoderValues = 1062,

	"""Send Early Bird Flag to parent device to hold device in bootloader."""
	BootloaderSetEarlyBirdFlag = 1070,

	"""Get bootable devices."""
	BootloaderGetBootableDevices = 1072,

	"""
	Shuts the controller down.
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| Int16			| 1 == shuts the controller down
	Get, GetDevInfo, GetValueList	| -				| not supported
	"""
	Shutdown = 1074,

	"""
	The identification number of the hardware board
	
	The command may add information for hardware components for certain miscellaneous tags (e.g. Param0, ...)
	
	Polytec::IO::CommandType		| Payload type	| Payload value
	--------------------------------|---------------|------------------
	Set								| -				| not supported
	Get, GetDevInfo, GetValueList	| Int32			| The ident number
	"""
	IdentNumber = 1080
