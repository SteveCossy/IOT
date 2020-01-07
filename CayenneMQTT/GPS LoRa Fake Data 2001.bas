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
 gosub RF_Tx:
 gosub RF_Tx:
 if w3 < 3100 then			'If battery flat then
  sleep 60					'go into a long deep sleep	
  goto Bat_Check				'and check thabattery again... 
 endif 

Lat_Deg:		
 b20 = 39
Lat_Raw_Min:		
 w11 = 26184 + time			'<<<<<<<<<<<<<<<<<<<<<<< Preset dummy lat minutes + time
Lat:
 serout 0,N2400_16,(#b20,46,#w11,13,10)

Lon_Deg:
 b21 = 173
Lon_Raw_Min:
 w12 = 55833 + time			'<<<<<<<<<<<<<<<<<<<<<<< Preset dummy lon minutes + time
Lon:
 serout 0,N2400_16,(#b21,44,#w12,13,10)
 
RF_Tx_Data:
  b9 = "G"					'Tx Lat
  w0 = b20
  gosub RF_Tx:
  b9 = "H"					'Tx Lat
  w0 = w11
  gosub RF_Tx:
  b9 = "I"					'Tx Lon
  w0 = b21
  gosub RF_Tx:
  b9 = "J"					'Tx Lon
  w0 = w12
  gosub RF_Tx:
  b9 = "K"					'Tx data
  w0 = time					'<<<<<<<<<<<<<<<<<<<<<<<<< Dummy Data = 'time' 
  gosub RF_Tx:

wait 1

loop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
RF_Tx:					'Main timing loop transmits every 4 to 6 seconds 
 b8  = "1"
 b9  = b9
 b10 = w0 // 256
 b11 = w0 /  256
 b12 = b8 XOR b9 XOR b10 XOR b11
 serout 0,N2400_16,(13,10,#w0,9)			'Debug script send pre data
 serout 0,N2400_16,(":0",b8,b9,b10,b11,b12)	'Debug script + Send Data Packet to the radio Tx'r

Lo_Ra_Tx:
 high 2							'Power Up LoRa
 nap 6
 serout 4,T2400_16,(":0",b8,b9,b10,b11,b12)	'Send Data Packet to the LoRa radio Tx'r
 nap 7
 low 2							'Power Down LoRa to save battery power
 nap 8		 					'Power Save pause for a few seconds while power is shut down
 nap 8
return
