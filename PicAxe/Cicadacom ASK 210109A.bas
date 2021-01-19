#Picaxe-08M2	'Directive to Chip Type
#Com 7		'Directive to Serial Port Number for programming and serial terminal monitoring
#Terminal 2400 	'Directive to set the Serial Terminal ro 4800 Baud
#No_Data		'Directive to NOT download EEPROM Data Table
DisableBOD		'Select uPower Sleep mode

Pre:
 high 1					'Preset TTL Logic Level to Pin 1 Data To Pi GPIO ttyAMA0
 b8  = "5" 	 				'Node ID as in :01 etc
 time = 123					'Preset clock
 tune 0,0,(21,22,23)			'Start Up Twinkle
 wait 3
 high 4
 
do 

RF_RX:
 serin 3,N2400,(":0",b8),b9,b10,b11,b12	'Listen for ":0X" and read in following 4 bytes
							'b9=Channel, b10 and b11 Lo and Hi byte data, b12 CSum
Check_Sum:
 b13 = b8 XOR b9 XOR b10 XOR b11 XOR b12	'Check data test using XOR
 serout 0,N2400,(13,10,"ASK  Rx Data ",":0",32,b8,32,#b9,32,#w5,32,#b12,9,"CS = ",#b13,13,10)	'Echo data to editor 
 'Echo result to programming lead to see what is happeing

Filter_Data_Packet: 
 if b13 = 0 then 	   			'If CSum result = GOOD = a zero then...
  gosub Post_Data				'Forward all data > Pi > Cayenne www
  inc b18					'Inc Good Data QoS counter
  toggle 2					'Good data TIC
  tune 0,0,(27)				'Optional annoying nice twinkle
 else						'Otherwise if Bad_Rx_Data: 
  inc b19					'Inc Bad QoS counter
  toggle 2					'Bad data TIC						
  pause 100					'Bad data TIC						
  toggle 2					'Bad data TIC					
  tune 0,3,(27,26,25)			'Optional annoying twinkle
 endif

Server_Data:
if time > 5 then				'If X seconds of processor time has elapsed then
 time = 1					'Reset the time ~ 5 to 10 minutes
 
Error_Updater:
 w5 = 0
 b9 = 22					'Set Channel: ID
 gosub Post_Data

Read_Temperature:				'Read DS18B20 on pin 4 IF fitted WPU = NO 4k7 resistor needed)
 'pokesfr %10001100, %00010000		'WPU Power ON selected Pins (NO 4k7 resistor needed)
 'readtemp12 4,w0				'Read HIGH resolution 12 bit DS18Btemperature by default
 'pokesfr %10001100, %00000000		'WPU Power OFF selected Pins
 'w0 = w0 * 10 / 16			'High Res = Decimal Deg C gives TENTHS of a degree Cee
 w5 = 222'w0
 b9 = 23					'Set Channel: ID
 gosub Post_Data
 
Read_Light:					'Read DS18B20 on pin 4 IF fitted WPU = NO 4k7 resistor needed)
 pokesfr %10001100, %00000100		'WPU Power ON selected Pins (NO 4k7 resistor needed)
 input 2
 pause 100
 readadc10 2, w0				'Read HIGH resolution 12 bit DS18Btemperature by default
 pokesfr %10001100, %00000000		'WPU Power OFF selected Pins
 w0 = 1024 - w0				'High Res = Decimal Deg C gives TENTHS of a degree Cee
 w5 = w0
 b9 = 24					'Set Channel: ID
 gosub Post_Data
 
QOS:
 inc b18					'Nominal starter QoS 1 percent
 w5 = b18+b19 				'Totalise all good and bad data packets
 w5 = b18 * 100 / w5			'Generate percentage 'Good'
 b18= 0
 b19 = 0
 b9 = 25					'Set Channel: ID
 gosub Post_Data
 
Bat_Volts:					'This is a method to infer battery voltage
 gosub mVcc					'Read a 1.024 volts internal refference voltage.  w10 = 25500 / w10             	'Rough calc b3 to 10'ths of a volt
 w5 = w12 / 10 * 10			'Round to nearest 10mV
 b9 = 26					'Set Channel: ID
 gosub Post_Data
 
endif

Q:
 if time <> b17 then
  b17 = time
  w5 = time
  b9 = 21					'Set Channel: ID
  gosub Post_Data
 endif

loop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Post_Data:
 b13 = b8 - 48 + b9 + w5 // 256		
 'Numeric Check Sum is hash byte total of Node + Channel + Data
 serout 1,T2400,(                ":0",44,b8,44,#b9,44,#w5,44,#b13,13,10)			
 'Tx Data packet to Pi
 serout 0,N2400,("Post Pi Data ",":0",44,b8,44,#b9,44,#w5,44,#b13,13,10)
 'Echo Local Data to Programming Lead
 nap 5					
 'Picaxe > Pi > Python Cayenne Min data rate
return

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
mVcc:				'CalibADC10 Picaxe Vcc mVolt Precisewise Linear Interpolator    
 calibadc10 w10		'Read a 1.024 volts internal refference voltage
 w10 = w10 MAX 420	'Set Max range 420 = ~ 2500 mV
 w10 = w10 MIN 165	'Set MIN range 165 = ~ 6.5 volts
 b22 = 420 - w10		'Calculate which EEPROM step value
 w12 = 2492			'Load Minimum range mV
 for b0 = 0 to b22	'Look up and ADD step values
  read b0,b23		'Lookup EEPROM step value
  w12 = w12 + b23		'Compound ADD to Minimum range mV
 next				'Until maximum calibadc10 step reached
 'w12 = 4444
 return
Data (0,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16,17,17,17,17,17,17,17,18,18,18,18,18,18,18,19,19,19,19,19,19,20,20,20,20,20,20,21,21,21,21,21,22,22,22,22,22,23,23,23,23,23,24,24,24,24,25,25,25,25,26,26,26,26,27,27,27,27,28,28,28,29,29,29,29,30,30,30,31,31,31,32,32,33,33,33,34,34,34,35,35,36,36,36,37,37,38,38)


