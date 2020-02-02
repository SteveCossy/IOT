'#Picaxe-08M2
'#Com 7
'Set com Port for programming and serial terminal monitoring
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
#No_Data
'Directive to prevent data table download
DisableBOD
'Select uPower Sleep mode

Pre:
 high 1						'Preset TTL Logic Level to Pin 1 Data To Pi GPIO ttyAMA0
 b8  = "1"  					'Node ID
 time = 123						'Advance clock for a faster initial Server Data Result
 tune 0,0,(21,22,23)				'Start Up Twinkle
 
do 

RF_RX:
 'serin 3,N2400,(":0",b8),b9,b10,b11,b12	'ASK  listen for ":0X" and read in following 5 bytes
 serin 3,T2400,(":0",b8),b9,b10,b11,b12	'LoRa Listen for ":0X" and read in following 5 bytes

Check_Sum:
 b13 = b8 XOR b9 XOR b10 XOR b11 XOR b12	'Check data with CSum
 serout 0,N2400,(13,10,"LoRa_RF_Rx= ",":0",b8,32,b9,32,#w5,32,#b13,13,10)	'Echo data to editor 

Good_Rx_Data: 
 if b13 = 0 then 				'If CSum result = GOOD = a zero 
  gosub Send_Data				'Go send the data to the Pi / Cayenne
  inc b21					'Inc QoS counter
  toggle 2					'Good data TIC
  'tune 0,0,(32,33,34)			'Optional annoying system BEEP if good data Rx
  'tune 0,0,(25,26,27)			'Optional annoying system BEEP if good data Rx

Bad_Rx_Data: 
 else						'Otherwise
  inc b22					'Bad data counter
  toggle 2					'Bad data TIC						
  pause 100					'Bad data TIC						
  toggle 2					'Bad data TIC					
  'tune 0,3,(34,33,32)			'Optional system BUZZ if bady data Rx
  tune 0,0,(27,26,25)			'Optional annoying system BEEP if good data Rx
 endif						

Server_Data:
 if time > 5 then				'Every few minutes of processor "time" has elapsed then
 time = 1					'Reset the time

Read_Temperature:				'Read DS18B20 on pin 4 IF fitted WPU = NO 4k7 resistor needed)
 pokesfr %10001100, %00010000		'WPU Power ON selected Pins (NO 4k7 resistor needed)
 readtemp12 4,w0				'Read HIGH resolution 12 bit DS18Btemperature by default
 pokesfr %10001100, %00000000		'WPU Power OFF selected Pins
 w0 = w0 * 10 / 16			'High Res = Decimal Deg C gives TENTHS of a degree Cee
 b9 = "W"
 w5 = w0
 b13 = 0					'Dummy Check Sum 
 gosub Send_Data				'Go send the data to the Pi / Cayenne
 
Read_Light:					'Read DS18B20 on pin 4 IF fitted WPU = NO 4k7 resistor needed)
 pokesfr %10001100, %00000100		'WPU Power ON selected Pins (NO 4k7 resistor needed)
 input 2
 pause 100
 readadc10 2, w0				'Read HIGH resolution 12 bit DS18Btemperature by default
 pokesfr %10001100, %00000000		'WPU Power OFF selected Pins
 w0 = 1024 - w0				'High Res = Decimal Deg C gives TENTHS of a degree Cee
 b9 = "X"
 w5 = w0
 b13 = 0					'Dummy Check Sum 
 gosub Send_Data				'Go send the data to the Pi / Cayenne

QOS:
 w5 = b21+b22 				'Totalise all good and bad data packets
 w5 = b21 * 100 / w5			'Generate percentage 'Good'
 b9 = "Y"
 b13 = 0					'Dummy Check Sum 
 gosub Send_Data				'Go send the data to the Pi / Cayenne
 b21 = 0
 b22 = 0

Bat_Volts:					'This is a method to infer battery voltage
 calibadc10 w5				'Read a 1.024 volts internal refference voltage.  w10 = 25500 / w10             	'Rough calc b3 to 10'ths of a volt
 w5 = 262 - w5 * 15 + 4000		'Approx 15 mV per calibadc10 count @ 4 Volts
 b9 = "Z"
 b13 = 0					'Dummy Check Sum 
 gosub Send_Data				'Go send the data to the Pi / Cayenne

endif

loop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Send_Data:					'Go send the data to the Pi / Cayenne
 serout 1,T2400,(":0",b8,44,b9,44,#w5,44,#b13,13,10)	'Tx CSV Data packet TTL to Pi
 serout 0,N2400,(":0",b8,44,b9,44,#w5,44,#b13,13,10)	'Tx CSV Data to USB Programming Lead
 nap 5								'Inter Packet Fixed Min Pacing delay
 return
