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

Bat_Check:					'Occasionally 
 calibadc10 w3				'Read a 1.024 volts internal refference voltage.  w10 = 25500 / w10             	'Rough calc b3 to 10'ths of a volt
 w3 = 262 - w3 * 15 + 4001		'Approx 15 mV per calibadc10 count @ 4 Volts
 b9 = "L"					'Tx battery mVolts
 w0 = w3
 gosub RF_Tx:
' if w3 < 3000 then
'  sleep 60
'  gosub RF_Tx:
'  gosub RF_Tx:
'  gosub RF_Tx:
'  goto Bat_Check
' endif 

Sensor_Data:
 readadc 1, w1
 b9 = "K"					'Tx data
 w0 = w1
 gosub RF_Tx:

loop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
RF_Tx:							'Main timing loop transmits every 4 to 6 seconds 
 b8  = "1"							'Node ID:
 b9  = b9							'Channel ID
 b10 = w0 // 256						'Low Data Byte
 b11 = w0 /  256						'High Data Byte	
 b12 = b8 XOR b9 XOR b10 XOR b11			'XOR Checksum
 serout 0,N2400_16,(13,10,#w0,9)			'Debug script send pre data
 serout 0,N2400_16,(":0",b8,b9,b10,b11,b12)	'Debug script + Send Data Packet to the radio Tx'r

Lo_Ra_Tx:
 high 2							'Power Up LoRa
 nap 6							'Power Up Warm Up time Delay
 serout 4,T2400_16,(":0",b8,b9,b10,b11,b12)	'Send Data Packet to the LoRa radio Tx'r
 nap 7							' Power Down delay to allow radio to finish transmitting data
 low 2							'Power Down LoRa to save battery power
 nap 8		 					'Power Save pause for a few seconds while power is shut down
 nap 8
return

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Fix:
 serin 3,T2400,("$GPRMC,"),#b0,#b0,b1
 serout 0,N2400_16,("Fix = ",b1,13,10)
 if b1 <> "A" then Fix
 serin 3,T2400,("$GPRMC,"),#b0,#b0,b1
 serout 0,N2400_16,("Fix = ",b1,13,10)
 if b1 <> "A" then Fix
 serin 3,T2400,("$GPRMC,"),#b0,#b0,b1
 serout 0,N2400_16,("Fix = ",b1,13,10)
 if b1 <> "A" then Fix
 return

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


'1 Deg Lat (m)	1 Deg Lon (m)
'111015.4548	86626.37279


