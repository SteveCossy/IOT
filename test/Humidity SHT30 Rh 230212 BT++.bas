'#Picaxe-08m2
'Chip type
'#Com 6
'Set com Port for programming and serial terminal monitoring
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
'#No_Data
'No data table download or wipe saves time
'Leaving the data table download in allows the battery indicator to work!
DisableBOD
'Select uPower Sleep mode
Setfreq m8
'Set clock frequency (and baud rate!)
nAmp:
pokesfr  %01110111,%00000011
'nAmp Drive

'WPU:
'pokesfr %10001100, %000000110	'Enable internal WPU Resistors
'Looks like not needed

Setup_I2C:
hi2csetup i2cmaster, %10000000, i2cslow_8, i2cbyte

serout 0,N9600_8,(CR,LF,"Giving Bluetooth time to start.")
pause 30000

'Send empty output packet to clear buffers
b19 = 0
w5 = 0
gosub RF_Tx:

time = 0					'Force inital Battery check

do
	gosub Humidity_sht30:
	gosub Temperature_sht30:
	b1 = time%5				'Every so often...  (%5 = run when time is a multiple of five minutes)
	if b1 = 0 then
		gosub Bat_Check:
	endif
	' Delay before next cycle
	' Period/Time Delay: 0/18ms, 1/36ms, 2/72ms, 3/144ms, 4/288ms, 5/576ms, 6/1.1s, 7/2.3s, 8/4s, 9/8s, 10/16s, 11/32s, 12/64s, 13/128s, 14/256s (4 mins)
	' Values from https://picaxe.com/basic-commands/time-delays/nap/#:~:text=The%20nap%20command%20puts%20the,is%20given%20by%20this%20table.
	nap 10				'Sub uAmp power saving DEEP Sleep
	serout 0,N9600_8,(CR,LF,"Finished napping at ",#time)
	inc time				'Use time variable to count packets
	if time > 253 then		'I don't want Time to take more than byte
		time = 0
	endif 
loop

Humidity_sht30:
CMD_WRITE_USER_REG_Rh:
  hi2cout 0x03,(%00000001)
  pause 100

CMD_READ_USER_REG:
  hi2cin 1,(b1)                         'Read HIGH Byte register
  hi2cin 2,(b0)                         'Read LOW  Byte register

Scale_Rh:
  w1 = w0 / 16                          'Bit shift Raw to Right
  w2 = w1 - 384
  w3 = w2 * 10 / 16

serout 0,N9600_8,(CR,LF,"   Humidity = ",#w3)

return

Temperature_sht30:
CMD_WRITE_USER_REG_Deg_C:
  hi2cout 0x03,(%00000000)
  pause 500

CMD_READ_USER_REG_Deg_C:
  hi2cin 1,(b1)                         'Read HIGH Byte register
  hi2cin 2,(b0)                         'Read LOW  Byte register

  w0 = w0 / 16
  w1 = w0 + 320                         'Bit shift Raw 14 bi XXXXXXXX
  w3 = w2 - 50                          'Refer to DSTH01 pdf pp6
  serout 0,N9600_8,(CR,LF,"Temperature = ",#w3)

return

Humidity:
'CMD_WRITE_USER_REG_Rh:
 hi2cout 0x03,(%00000001)
 pause 100

'CMD_READ_USER_REG:
 hi2cin 1,(b1)				'Read HIGH Byte register
 hi2cin 2,(b0)				'Read LOW  Byte register
 
Test_Bits_Rh: 
'serout 0,N2400,(#bit15,#bit14,#bit13,#bit12,#bit11,#bit10,#bit9,#bit8,32,#bit7,#bit6,#bit5,#bit4,#bit3,#bit2,#bit1,#bit0,13,10)

'Scale_Rh:
 w1 = w0 / 16				'Bit shift Raw 12 bit XXXXXXXX XXXXnnnn word 4 bits to Right
 w2 = w1 - 384				'Refer to DSTH01 pdf pp6  %RH = (RH/16)-24,
 w3 = w2 * 10 / 16			'Refer to DSTH01 pdf pp6  %RH = (RH/16)-24,
' serout 0,N9600_8,(13,10,"Humidity = ",#w3)
 b19 = 9
 w5 = w3
gosub RF_Tx:
return

Temperature:
'CMD_WRITE_USER_REG_Deg_C:
 hi2cout 0x03,(%00010001)
 pause 100

'CMD_READ_USER_REG_Deg_C:
 hi2cin 1,(b1)				'Read HIGH Byte register
 hi2cin 2,(b0)				'Read LOW  Byte register
 
Test_Bits_Deg_C: 
' serout 0,N2400,(#bit15,#bit14,#bit13,#bit12,#bit11,#bit10,#bit9,#bit8,32,#bit7,#bit6,#bit5,#bit4,#bit3,#bit2,#bit1,#bit0,13,10)
 w1 = w0 / 4				'Bit shift Raw 14 bi XXXXXXXX XXnnnnnn word 4 bits to Right
 w2 = w1 * 10 / 32	 			'Refer to DSTH01 pdf pp6  Temperature(?C) = (TEMP/32)-50
 w3 = w2 -500	 			'Refer to DSTH01 pdf pp6  Temperature(?C) = (TEMP/32)-50
' serout 0,N9600_8,(13,10,"Temperature = ",#w3)
 b19 = 10
 w5 = w3
 gosub RF_Tx:
 return

Bat_Check:

  gosub mVcc
'  serout 0,N2400,(13,10,#w12)
  b19 = 26
  w5 = w12 / 100 * 100 + 09			'Rough calc b3 to 10'ths of a volt
  gosub RF_Tx:						'Go and Tx the Data via Radio IF fitted
  return
  
;=======================================================================================
Sub_Routines:

RF_Tx:
 b18 = "1"													'Set 'Cicadacom' Node ID
 b19 = b19													'Set Cayenne Channel number
 b20 = w5 // 256												'Data Low Byte
 b21 = w5 /  256												'Data High Byte
 b22 = b18 XOR b19 XOR b20 XOR b21								'Generate simple single byte hash XOR Check Sum 
 serout 0,N9600_8,(CR,LF,#time,32,#b19,9,#w5,9,#b21,32,#b20,9)	'Optional human read-able view data being exported to RF module
' serout 4,T9600_8,(13,10,#time,32,#b19,9,#w5,9,#b21,32,#b20,9)	'Output to HCO5 BT module from old code
 serout 4,T9600_8,(CR,LF,#time,32,#b19,9,#w5,9,#b22)	'Output to HCO5 BT module
 'serout 0,N2400,(85,85,85,":0",b18,b19,b20,b21,b22)				'RF ASK preamble followed by Synch Chars :0, NodeID, Channel#, DataL, DataH,C.Sum

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
 
