'#Picaxe-08m2
'Chip type
'#Com 1
'Set com Port for programming and serial terminal monitoring
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
#No_Data
'No data table download or wipe saves time
DisableBOD
'Select uPower Sleep mode
Setfreq m8
'Set clock frequency (and baud rate!)
nAmp:
pokesfr  %01110111,%00000011
'nAmp Drive

'WPU:
'pokesfr %10001100, %000000110						'Enable internal WPU Resistors
'Looks like not needed

Setup_I2C:
hi2csetup i2cmaster, %10000000, i2cfast, i2cbyte

do

CMD_WRITE_USER_REG_Rh:
 hi2cout 0x03,(%00000001)
 pause 100

CMD_READ_USER_REG:
 hi2cin 1,(b1)				'Read HIGH Byte register
 hi2cin 2,(b0)				'Read LOW  Byte register
 
Test_Bits_Rh: 
'serout 0,N2400,(#bit15,#bit14,#bit13,#bit12,#bit11,#bit10,#bit9,#bit8,32,#bit7,#bit6,#bit5,#bit4,#bit3,#bit2,#bit1,#bit0,13,10)

Scale_Rh:
 w1 = w0 / 16				'Bit shift Raw 12 bit XXXXXXXX XXXXnnnn word 4 bits to Right
 w2 = w1 - 384				'Refer to DSTH01 pdf pp6  %RH = (RH/16)-24,
 w3 = w2 * 10 / 16			'Refer to DSTH01 pdf pp6  %RH = (RH/16)-24,
 serout 0,N9600_8,(13,10,"Humidity = ",#w3)
 b19 = 9
 w5 = w3
 serout 4,T9600_8,(13,10,#time,32,#b19,9,#w5,9,#b21,32,#b20,9)	'Output to HCO5 BT module
 nap 5

CMD_WRITE_USER_REG_Deg_C:
 hi2cout 0x03,(%00010001)
 pause 100

CMD_READ_USER_REG_Deg_C:
 hi2cin 1,(b1)				'Read HIGH Byte register
 hi2cin 2,(b0)				'Read LOW  Byte register
 
Test_Bits_Deg_C: 
' serout 0,N2400,(#bit15,#bit14,#bit13,#bit12,#bit11,#bit10,#bit9,#bit8,32,#bit7,#bit6,#bit5,#bit4,#bit3,#bit2,#bit1,#bit0,13,10)
 w1 = w0 / 4				'Bit shift Raw 14 bi XXXXXXXX XXnnnnnn word 4 bits to Right
 w2 = w1 * 10 / 32	 			'Refer to DSTH01 pdf pp6  Temperature(?C) = (TEMP/32)-50
 w3 = w2 -500	 			'Refer to DSTH01 pdf pp6  Temperature(?C) = (TEMP/32)-50
 serout 0,N9600_8,(13,10,"Temperature = ",#w3)
 b19 = 10
 w5 = w3
 serout 4,T9600_8,(13,10,#time,32,#b19,9,#w5,9,#b21,32,#b20,9)	'Output to HCO5 BT module
 nap 5
  
loop
