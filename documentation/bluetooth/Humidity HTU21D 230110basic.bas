#Picaxe-08m2
'Chip type
#Com 1
'Set com Port for programming and serial terminal monitoring
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
#No_Data
'No data table download or wipe saves time
DisableBOD
'Select uPower Sleep mode
Setfreq m4
'Set clock frequency (and baud rate!)

'All the above are optional programmer environment setting commands
'Refer to data sheet HTU21D.pdf

Enable_WPU:
pokesfr %10001100, %000000110       
'Enables weak pull up virtual resistors ON Pins 1 and 2

Setup_I2C:
hi2csetup i2cmaster, %10000000, i2cfast, i2cbyte
'Config picaxe i2c modes 
wait 1

'CMD_SOFT_RESET= 0xfe
hi2cout %10000000,($FE)
'Init, and reset HTU21D
pause 500

'CMD_READ_USER_REG = 0xe7
'hi2cin 0xE7,(b0)
'Optional read back config register bits
'sertxd (#bit7,#bit6,#bit5,#bit4,#bit3,#bit2,#bit1,#bit0,13,10)
'pause 100

'CMD_WRITE_USER_REG = 0xe6
hi2cout 0xE6,(%00000010)		
'Write to user register
pause 100					

'CMD_READ_USER_REG = 0xe7 to see if any changes were stored / took place
'hi2cin 0xE7,(b0)
'Optional read back register
'sertxd (#bit7,#bit6,#bit5,#bit4,#bit3,#bit2,#bit1,#bit0,13,10)
'pause 100

do						'Main loop starts here

'CONVERSION OF SIGNAL OUTPUTS  
'Default resolution is set to 12-bit relative humidity and 14-bit temperature readings.
'Measured data are transferred in two byte packages, i.e. in frames of 8-bit length 
'where the most significant bit (MSB) is transferred first (left aligned). 
'Each byte is followed by an acknowledge bit. The two status bits, 
'the  last bits of LSB, must be set to ‘0’ before calculating physical values. 

Temperature:
 hi2cin 0xE3,(b1,b0)			'MSB,LSB 'CMD_READ_TEMP_HOLD = 0xe3
 'Read IN Temperature b1 and b0 bytes to make data WORD 'w0'
 w1 = w0 / 256
 w2 = w1 * 176
 w3 = w2 / 256
 w4 = w3 - 47
 'serout 0,N2400,(13,10,#w4)
 'Optional terminal test point

RF_Tx_Temperature_Deg_C:
 b19 = 9
 w5 = w4
 gosub RF_Tx:		'Go and Tx the Data via Radio IF fitted

Humidity:
 hi2cin 0xE5,(b1,b0)			'MSB,LSB 'CMD_READ_HUM_HOLD = 0xe5
 'Read IN Humidity b1 and b0 bytes to make data WORD 'w0'
 w1 = w0 / 256
 w2 = w1 * 125
 w3 = w2 / 256
 w4 = w3 - 6
 'serout 0,N2400,(13,10,#w4)
 'Optional terminal test point

RF_Tx_Humidity_Rh:
 b19 = 10
 w5 = w4
 gosub RF_Tx:						'Go and Tx the Data via Radio IF fitted

Bat_Check:
 if time > 5 then					'Every so often...
  time = 1
  gosub mVcc
  serout 0,N2400,(13,10,#w12)
  b19 = 26
  w5 = w12 / 100 * 100 + 09			'Rough calc b3 to 10'ths of a volt
  gosub RF_Tx:						'Go and Tx the Data via Radio IF fitted
 endif 
 
loop

;=======================================================================================
Sub_Routines:

RF_Tx:
 b18 = "1"														'Set 'Cicadacom' Node ID
 b19 = b19														'Set Cayenne Channel number
 b20 = w5 // 256												'Data Low Byte
 b21 = w5 /  256												'Data High Byte
 b22 = b18 XOR b19 XOR b20 XOR b21								'Generate simple single byte hash XOR Check Sum 
 'serout 0,N2400,(13,10,#time,32,#b19,9,#w5,9,#b21,32,#b20,9)	'Optional human read-able view data being exported to RF module
 serout 0,N2400,(85,85,85,":0",b18,b19,b20,b21,b22)				'RF ASK preamble followed by Synch Chars :0, NodeID, Channel#, DataL, DataH,C.Sum
 nap 8															'Sub uAmp power saving short DEEP Sleep (nap) ~ 2 Seconds 	
 nap 8															'Sub uAmp power saving short DEEP Sleep (nap) ~ 2 Seconds
 nap 8															'Sub uAmp power saving short DEEP Sleep (nap) ~ 2 Seconds
 return															'Play it again Sam

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
mVcc:				'CalibADC10 Picaxe Vcc mVolt Precisewise Linear Interpolator   
 calibadc10 w10		'Read a 1.024 volts internal refference voltage. 
 w10 = w10 MAX 420	'Set Max range 420 = ~ 2500 mV
 w10 = w10 MIN 165	'Set MIN range 165 = ~ 6.5 volts
 b22 = 420 - w10		'Calculate which EEPROM step value
 w12 = 2492			'Load Minimum range mV
 for b0 = 0 to b22	'Look up and ADD step values
  read b0,b23		'Lookup EEPROM step value
  w12 = w12 + b23		'Compound ADD to Minimum range mV
 next				'Until maximum calibadc10 step reached
 return 
 Data (0,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16,17,17,17,17,17,17,17,18,18,18,18,18,18,18,19,19,19,19,19,19,20,20,20,20,20,20,21,21,21,21,21,22,22,22,22,22,23,23,23,23,23,24,24,24,24,25,25,25,25,26,26,26,26,27,27,27,27,28,28,28,29,29,29,29,30,30,30,31,31,31,32,32,33,33,33,34,34,34,35,35,36,36,36,37,37,38,38)

