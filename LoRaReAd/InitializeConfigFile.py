"""
    Initialize the Config file using User inputs.
    This Config file is written in TOML, and contatins
    authentication information for Cayenne, channel names
    and divisors, and thresholds for fine-tuning the error 
    detection and penguin detection algororthms
"""

import toml, os, uuid
from UsefulConstants import ReturnDict

def WriteFile(MQTTUser, MQTTPass, MQTTClientID):
	# Useful constants
	CD = ReturnDict()
	# Extracting the constants need for this file
	Eq = CD['Eq']
	Qt = CD['Qt']
	CrLf = CD ['CrLf']

	FileName = CD['HomeDir'] + CD['ConfFile']

	# Create a unique ID for the Python program
	# based on the MAC address of the Pi
	MAC = hex(uuid.getnode())

	UniqueIDk      = 'UniqueID' + Eq
	UniqueIDd      = Qt + 'PythonClient' + MAC + Qt

	MQTTSection    = '[MQTTCredentials]'
	MQTTBlurb1     = '# This section is used to store credentials necessary to connect to the Cayenne Dashboard'
	MQTTBlurb2     = '# The credentials are provided by Cayenne when setting up a new custom device'

	MQTTUserk      = 'MQTTUsername' + Eq
	MQTTUserd      = Qt + MQTTUser + Qt

	MQTTPassk      = 'MQTTPassWord' + Eq
	MQTTPassd      = Qt + MQTTPass + Qt

	MQTTClientk    = 'MQTTClientID' + Eq
	MQTTClientd    = Qt + MQTTClientID + Qt

	# Sets the detection threshold to a user-set number
	# Used for fine-tuning in case of diffent species or environments and for initial set-up
	DetectSection  = '[DetectionThresholds]'
	DetectBlurb    = '# This section is used to hold thresholds for error detection and penguin detection algorithms'

	DetectThreshk  = 'DetectThresh' + Eq
	DetectThreshd  = Qt + '2' + Qt

	# Sets the difference threshold to a user-set number
	ErrThreshk     = 'ErrThresh' + Eq
	ErrThreshd     = Qt + '20' + Qt

	# Information for the chanels that are used

	# Channels need to be changed somewhat to allow for multiple incoming sensors
	# In conversations with Andrew, a single mound can have 4 different temp sensor, and other data channels like battery voltage
	# Multiple Picaxe modules can attach to a single Pi
	# eg. Mound1 temp1/temp2/temp3/temp4/mAmps, Mound2 etc

	# Channels with unusual divisors
	ChannelSection   = '[ChannelDivisors]'
	ChannelBlurb     = '# This section is to be used to store any divisor needed to alter the data into a useable range'

	Channel1k     = 'Channel1' + Eq
	Channel1d     = Qt + '10' + Qt

	Channel2k     = 'Channel2' + Eq
	Channel2d     = Qt + '10' + Qt

	Channel3k     = 'Channel3' + Eq
	Channel3d     = Qt + '10' + Qt

	Channel4k     = 'Channel4' + Eq
	Channel4d     = Qt + '10' + Qt

	Channel5k     = 'Channel5' + Eq
	Channel5d     = Qt + '1' + Qt

	Channel6k     = 'Channel6' + Eq
	Channel6d     = Qt + '10' + Qt

	Channel7k     = 'Channel7' + Eq
	Channel7d     = Qt + '10' + Qt

	Channel8k     = 'Channel8' + Eq
	Channel8d     = Qt + '10' + Qt

	Channel9k     = 'Channel9' + Eq
	Channel9d     = Qt + '10' + Qt

	Channel10k    = 'Channel10' + Eq
	Channel10d    = Qt + '1' + Qt

	Channel11k    = 'Channel11' + Eq
	Channel11d    = Qt + '10' + Qt

	Channel12k    = 'Channel12' + Eq
	Channel12d    = Qt + '10' + Qt

	Channel13k    = 'Channel13' + Eq
	Channel13d    = Qt + '10' + Qt

	Channel14k    = 'Channel14' + Eq
	Channel14d    = Qt + '10' + Qt

	Channel15k    = 'Channel15' + Eq
	Channel15d    = Qt + '1' + Qt

	Channel16k    = 'Channel16' + Eq
	Channel16d    = Qt + '10' + Qt

	Channel17k    = 'Channel17' + Eq
	Channel17d    = Qt + '10' + Qt

	Channel18k    = 'Channel18' + Eq
	Channel18d    = Qt + '10' + Qt

	Channel19k    = 'Channel19' + Eq
	Channel19d    = Qt + '10' + Qt

	Channel20k    = 'Channel20' + Eq
	Channel20d    = Qt + '1' + Qt

	Channel21k    = 'Channel21' + Eq
	Channel21d    = Qt + '10' + Qt

	Channel22k    = 'Channel22' + Eq
	Channel22d    = Qt + '10' + Qt

	Channel23k    = 'Channel23' + Eq
	Channel23d    = Qt + '10' + Qt

	Channel24k    = 'Channel24' + Eq
	Channel24d    = Qt + '10' + Qt

	Channel25k    = 'Channel25' + Eq
	Channel25d    = Qt + '1' + Qt

	Channel26k    = 'Channel26' + Eq
	Channel26d    = Qt + '1' + Qt

    # further calibration values could be used to modify incoming data to offset wonky sensors

	OffsetSection  = '[OffsetValues]'
	OffsetBlurb    = '# This section is used to store values for offsetting any calibration issues in temperature sensors'

	OffsetExample  = '# Possible framework:'
	OffsetExamplek = '#Offset1' + Eq
	OffsetExampled = '#Offset1'

	Opening  = '# Configuration settings to connect to Cayenne and store specific info for individual channels'
	Closing  = '# This file was created by ' + UniqueIDd

	TomlString = Opening + CrLf \
		+ MQTTSection + CrLf \
		+ MQTTBlurb1 + CrLf \
		+ MQTTBlurb2 + CrLf \
		+ MQTTUserk + MQTTUserd + CrLf \
		+ MQTTPassk + MQTTPassd + CrLf \
		+ MQTTClientk + MQTTClientd + CrLf \
		+ UniqueIDk + UniqueIDd + CrLf \
		+ DetectSection + CrLf \
		+ DetectBlurb + CrLf \
  		+ DetectThreshk + DetectThreshd + CrLf \
		+ ErrThreshk + ErrThreshd + CrLf \
		+ ChannelSection + CrLf \
		+ ChannelBlurb \
		+ Channel1k + Channel1d + CrLf \
		+ Channel2k + Channel2d + CrLf \
		+ Channel3k + Channel3d + CrLf \
		+ Channel4k + Channel4d + CrLf \
		+ Channel5k + Channel5d + CrLf \
		+ Channel6k + Channel6d + CrLf \
		+ Channel7k + Channel7d + CrLf \
		+ Channel8k + Channel8d + CrLf \
		+ Channel9k + Channel9d + CrLf \
		+ Channel10k + Channel10d + CrLf \
		+ Channel11k + Channel11d + CrLf \
		+ Channel12k + Channel12d + CrLf \
		+ Channel13k + Channel13d + CrLf \
		+ Channel14k + Channel14d + CrLf \
		+ Channel15k + Channel15d + CrLf \
		+ Channel16k + Channel16d + CrLf \
		+ Channel17k + Channel17d + CrLf \
		+ Channel18k + Channel18d + CrLf \
		+ Channel19k + Channel19d + CrLf \
		+ Channel20k + Channel20d + CrLf \
		+ Channel21k + Channel21d + CrLf \
		+ Channel22k + Channel22d + CrLf \
		+ Channel23k + Channel23d + CrLf \
		+ Channel24k + Channel24d + CrLf \
		+ Channel25k + Channel25d + CrLf \
		+ Channel26k + Channel26d + CrLf \
		+ OffsetSection + CrLf \
		+ OffsetBlurb + CrLf \
		+ OffsetExamplek + OffsetExampled + CrLf \
		+ Closing

	ParsedToml = toml.loads(TomlString)

	OutFile = open(FileName, "w")
	toml.dump(ParsedToml, OutFile)
	OutFile.close