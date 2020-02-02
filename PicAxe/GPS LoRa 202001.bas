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
 if w3 < 3000 then
  sleep 60
  gosub RF_Tx:
  gosub RF_Tx:
  gosub RF_Tx:
  goto Bat_Check
 endif 

Sensor_Data:
 inc time
 w3 = time
 b9 = "K"					
 w0 = w3
 gosub RF_Tx:				'Tx data once per cycle

GPS_Power_ON:
 high 1					'Power Up GPS

gosub Fix:

Lat:
 serin  3,T2400,("$GPRMC,"),#b0,#b0,b0,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10

Calc_Lat_Raw_Min:		
 b20 = b1 - 48 * 10			;Tens of Deg Latitude
 b20 = b2 - 48 * 1 + b20		;Ones of Deg Latitude

 w11 = b3 - 48 * 10000			'Tens of Minutes Lattitude
 w11 = b4 - 48 * 1000  + w11		'Ones of Minutes Lattitude
 w11 = b6 - 48 * 100   + w11		'Tenths of Minutes Lattitude
 w11 = b7 - 48 * 10    + w11		'Hundredths of Minutes Lattitude
 w11 = b8 - 48 * 1     + w11		'Thoutandths of Minutes Lattitude
 w11 = b9 - 48 * 1 / 5 + w11		'Rounded ten thousandths of Minutes Lattitude
 
 serout 0,N2400_16,(b1,b2,46,b3,b4,b5,b6,b7,b8,b9,b10,9,#b20,44,#w11,13,10)
;                   4   1  .  1  7  .  1  0  2  9   6	   39   ,  1029
; e.g.41.284975°

Lon:
 serin 3,T2400,("$GPRMC,"),#b0,#b0,b0,#b0,#b0,b0,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11

Calc_Lon_m:
 b21 = b1 - 48 * 100			;Tens of Deg Lon
 b21 = b2 - 48 * 10 + b21		;Ones of Deg Lon
 b21 = b3 - 48 * 1  + b21		;Ones of Deg Lon

 w12 = b4  - 48 * 10000
 w12 = b5  - 48 * 1000  + w12
 w12 = b7  - 48 * 100   + w12
 w12 = b8  - 48 * 10    + w12
 w12 = b9  - 48 * 1     + w12
 w12 = b10 - 48 * 1 / 5 + w12
 
 serout 0,N2400_16,(b1,b2,b3,46,b4,b5,b6,b7,b8,b9,b10,b11,9,#b21,44,#w12,13,10)
'                    1  7  4  .  4  3  .  7  0  1   1   5	7011
'174.728426°
 
 
GPS_Power_OFF:
 low 1
 serout 0,N2400_16,(13,10)

RF_Tx_Data:
 b9 = "G"					'Tx Lat Deg once per cycle
 w0 = b20
 gosub RF_Tx:
 b9 = "I"					'Tx Lon Deg once per cycle
 w0 = b21
 gosub RF_Tx:
 for b27 = 1 to 2				'Repeat GPS detail data 
  b9 = "H"					'Tx Lat Min
  w0 = w11
  gosub RF_Tx:
  b9 = "J"					'Tx Lon Min
  w0 = w12
  gosub RF_Tx:
 next b27

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


