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

	UniqueIDk      = 'UniqueID'+Eq
	UniqueIDd      = Qt + 'PythonClient' + MAC + Qt

	MQTTSection    = '[MQTTCredentials]'

	MQTTUserk      = 'MQTTUsername'
	MQTTUserd      = Qt + MQTTUser + Qt

	MQTTPassk      = 'MQTTPassWord'
	MQTTPassd      = Qt + MQTTPass + Qt

	MQTTClientk    = 'MQTTClientID'
	MQTTClientd    = Qt + MQTTClientID + Qt

	# Sets the increase threshold to a user-set number
	# Used for fine-tuning in case of diffent species or environments and for initial set-up
	DetectSection  = '[DetectionThresholds]'

	DetectThreshk  = 'DetectThresh' + Eq
	DetectThreshd  = Qt + 2 + Qt

	# Sets the difference threshold to a user-set number
	ErrThreshk     = 'ErrThresh' + Eq
	ErrThreshd     = Qt + 20 + Qt

	# Information for the chanels that are used

	# Channels with unusual divisors
	ChannelSection = '[ChannelDivisors]'

	Channel10n     = 'Channel10'
	Channel10d     = '60000'

	Channel11n     = 'Channel11'
	Channel11d     = '60000'

	Channel23n     = 'Channel23'
	Channel23d     = '10'

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
		+ Channel10n + Channel10d + CrLf \
		+ Channel11n + Channel11d + CrLf \
		+ Channel23n + Channel23d + CrLf \
		+ Closing

	ParsedToml = toml.loads(TomlString)

	OutFile = open(FileName, "w")
	toml.dump(ParsedToml, OutFile)
	OutFile.close