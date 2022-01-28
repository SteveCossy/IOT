"""
    Initialize the Config file using User inputs.
    This Config file is written in TOML, and contatins
    authentication information for Cayenne, channel names
    and divisors, and thresholds for fine-tuning the error 
    detection and penguin detection algororthms
"""

import toml, os, uuid


def WriteFile(MQTTUser, MQTTPass, MQTTClientID):
	# Useful constants
	Eq	= ' = '
	CrLf	= '\r\n'
	Qt	= '"'
	HomeDir =    os.environ['HOME']
	CsvPath =      HomeDir+'/'
	CSV =           '.csv'

	FileName = HomeDir + '/MQTT Config'

	# Create a unique ID for the Python program
	# based on the MAC address of the Pi
	MAC = hex(uuid.getnode())

	UniqueIDk      = 'UniqueID' + Eq
	UniqueIDd      = Qt + 'PythonClient' + MAC + Qt

	MQTTSection    = '[MQTTCredentials]'

	MQTTUserk      = 'MQTTUsername' + Eq
	MQTTUserd      = Qt + MQTTUser + Qt

	MQTTPassk      = 'MQTTPassWord' + Eq
	MQTTPassd      = Qt + MQTTPass + Qt

	MQTTClientk    = 'MQTTClientID' + Eq
	MQTTClientd    = Qt + MQTTClientID + Qt

	# Sets the detection threshold to a user-set number
	# Used for fine-tuning in case of diffent species or environments and for initial set-up
	DetectSection  = '[DetectionThresholds]'

	DetectThreshk  = 'DetectThresh' + Eq
	DetectThreshd  = Qt + '2' + Qt

	# Sets the difference threshold to a user-set number
	ErrThreshk     = 'ErrThresh' + Eq
	ErrThreshd     = Qt + '20' + Qt

	# Information for the chanels that are used

	# Channels need to be changed somewhat to allow for multiple incoming sensors
	# In conversations with Andrew, a single mound can have 4 different temp sensor, and other sensors, like voltage and light

	# Channels with unusual divisors
	ChannelSection = '[ChannelDivisors]'

	Channel10k     = 'Channel10' + Eq
	Channel10d     = Qt + '60000' + Qt

	Channel11k     = 'Channel11' + Eq
	Channel11d     = Qt + '60000' + Qt

	Channel23k     = 'Channel23' + Eq
	Channel23d     = Qt + '10' + Qt

    # further calibration values could be used to modify incoming data to offset wonky sensors

	Opening  = '# Configuration settings to connect to Cayenne and store specific info for individual channels'
	Closing  = '# This file was created by '

	TomlString = Opening + CrLf \
		+ MQTTSection + CrLf \
		+ MQTTUserk + MQTTUserd + CrLf \
		+ MQTTPassk + MQTTPassd + CrLf \
		+ MQTTClientk + MQTTClientd + CrLf \
		+ UniqueIDk + UniqueIDd + CrLf \
		+ DetectSection + CrLf \
  		+ DetectThreshk + DetectThreshd + CrLf \
		+ ErrThreshk + ErrThreshd + CrLf \
		+ ChannelSection + CrLf \
		+ Channel10k + Channel10d + CrLf \
		+ Channel11k + Channel11d + CrLf \
		+ Channel23k + Channel23d + CrLf \
		+ Closing

	ParsedToml = toml.loads(TomlString)

	OutFile = open(FileName, "w")
	toml.dump(ParsedToml, OutFile)
	OutFile.close