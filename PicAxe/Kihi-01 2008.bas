#Picaxe-08M2
#Com 7
'Set com Port for programming and serial terminal monitoring
'#Terminal 9600
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
DisableBOD
'Select uPower Sleep mode
#No_Data
'Do not down load or wipe the data table
Setfreq m16
'Double clock Freq to give seertxd data rate of 9600 Baud

Presets:
 high 4
 low 1

do

Moisture_Sensor_Data_1a:
 pokesfr %10001100, %00001000		'WPU Power ON via 1 Meg Ohm selected Pin(s)
 readadc10 1, w1				'Read Voltage on sensor pin
 pokesfr %10001100, %00000000		'WPU Power OFF selected Pin(s)
 w1 = 1024 - w1 / 2 * 2 + 1		'Odd or Even low range moisture sensor (ODD LSB)

Moisture_Sensor_Data_1b:
 if w1 > 1000 then
  pokesfr %10001100, %00000010	'WPU Power directly ON to selected Pin(s)
  readadc10 1, w1				'Read Voltage on sensor pin
  pokesfr %10001100, %00000000	'WPU Power OFF selected Pin(s)
  w1 = 1024 - w1 / 2 * 2 + 0		'Odd or Even low range moisture sensor (EVEN LSB)
 endif
 w0 = w1					'Invert to get a positive going 'Moisture Level'
 b9 = "A"					'Tx data
 gosub RF_Tx:

Sensor_Data_2:
Read_Sensors:
 pokesfr %10001100, %00000100		'WPU Power ON selected Pin(s)
 readtemp12 2, w2				'Read DS18B20 high resolution
 pokesfr %10001100, %00000000		'WPU Power OFF selected Pins readadc 1, w1
 w0 = w2 * 10 / 16			'Scale 12 bit temperature to one place decimal Deg C
 b9 = "B"					'Tx data
 gosub RF_Tx:

Sequence_Data_3:				'Cycle Time Counter for QoS calculation
 inc time					'Bump up the nominal 'time' counter word variable by one count
 b9 = "C"					'Tx data
 w0 = time
 gosub RF_Tx:

Bat_Check:					'Occasionally 
 calibadc10 w3				'Read a 1.024 volts internal refference voltage.
 w3 = 262 - w3 * 15 + 4000		'Calculate rough mVolts 
 b9 = "D"					'Tx battery mVolts
 w0 = w3
 gosub RF_Tx:

Low_Volt_Standby:				'Go to sleep if mVolts are too low to save battery
 if w3 < 3000 then			'If the battery drops to 3 Volts then it is flat
  sleep 60					'Take a LONG sleep to rest things
  gosub RF_Tx:				'Transmit present voltage
  gosub RF_Tx:				'Several times
  gosub RF_Tx:				'Then
  goto Bat_Check				'Check battery voltage again
 endif 					'Until sun comes out or battery volts recover 

loop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
RF_Tx:							'Main timing loop transmits every 4 to 6 seconds 
 b8  = "1"							'Node ID:
 b9  = b9							'Channel ID
 b10 = w0 // 256						'Low Data Byte
 b11 = w0 /  256						'High Data Byte	
 b12 = b8 XOR b9 XOR b10 XOR b11			'XOR Checksum
 'serout 0,N2400_16,(13,10,13,10,#w0,9,b9,9)			'Debug script send pre data
 'serout 0,N2400_16,(":0",b8,b9,b10,b11,b12)	'Debug script + Send Data Packet to the radio Tx'r

Lo_Ra_Tx:
 high 0							'Power Up LoRa
 nap 3							'Power Up Warm Up time Delay
 nap 2							'Power Up Warm Up time Delay
 serout 4,T2400_16,(":0",b8,b9,b10,b11,b12)	'Send Data Packet to the LoRa radio Tx'r
 nap 5							'Power Down delay to allow radio to finish transmitting data
 nap 4							'Power Down delay to allow radio to finish transmitting data
 nap 3							'Power Down delay to allow radio to finish transmitting data
 nap 2							'Power Down delay to allow radio to finish transmitting data
 if w3 < 4100 then					'IF the system starts to 'Over Volt' then leave LoRa powered up
  low 0							'Power Down LoRa to save battery power
 endif							'IF the system starts to 'Over Volt' then leave LoRa powered up
 nap 7		 					'Power Save pause for a few seconds
 nap 8		 					'Power Save pause for a few seconds
 nap 8		 					'Power Save pause for a few seconds
 nap 8		 					'Power Save pause for a few seconds
return							

