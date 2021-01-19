#PICAXE 08M2
#Com 7
'Set com Port for programming and serial terminal monitoring
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
'#No_Data
'Directive to prevent data table download
DisableBOD
'Select uPower Sleep mode

Pre:
 sleep 1
 high 1					'Preset TTL Logic Level to Pin 1 Data To Pi GPIO ttyS0
 b8  = "1"  				'Set Node ID as in :0"X" etc
 gosub mVcc					'Go check the battery voltage
 high 4
 
do 

Picaxe_Clock:
 sleep 1					'Pi Running Tick Rate
 pause 10					'Fine tune the Picaxe Clock
 serout 0,N2400,(13,10,"Pi Running = ",#pin4,9,#pin2,9,"Time = ",#time)

Send_System_Data:
if time <> w13 then			'If 08M2 processor time has changed then
	 w13 = time				'Update present time 
	 Test_Data:					'Send the present 08M2 time to Cayenne
	  w5 = time
	  b8 = b8					'Set NODE: ID
	  b9 = "Y"					'Set Channel: ID
	  b13 = 0					'Dummy Check Sum 
	  gosub Post_Data
	  gosub Post_Data
	 Bat_Volts:					'Send the Battery mV to Cayenne
	  gosub mVcc
	  w5 = w12
	  b8 = b8					'Set NODE: ID
	  b9 = "Z"					'Set Channel: ID
	  b13 = 0					'Dummy Check Sum 
	  gosub Post_Data
	  gosub Post_Data
 endif

Pi_Hibernator:
 if pin2 = 0 OR time > 25 then					'IF Pi Data Pin low Pi has shut down !
  gosub mVcc								'Check the Battery Voltage
  serout 0,N2400,(13,10,"Pi Shutting Down")			'OR if Pi running > 20 then...
  sleep 10									'Allow Pi Tidy and Complete ShutDown
  low 4									'Turn OFF DC power supply to Pi
  serout 0,N2400,(13,10,"Pi DC Power = OFF")
  for w0 = 1 to 2'300'600'1500						'Wait for 300 = 10 min ~ 1500 = 50 minutes
   serout 0,N2400,(13,10,"System is uAmp Sleeping",9,#w0)	'Echo Sleeping State
   sleep 1									'Sleep cycle tick rate
  next 
  time = 0									'Reset the Time 
 endif
 
Pi_Start_Up:
 if pin4 = 0 then								'IF Pi is already Shut Down then...
  gosub mVcc								'Check the Battery Voltage
  if w12 > 4000 then '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''5100 then							'IF Battery = Good then...
   high 4									'Switch ON battery Power to Pi
   serout 0,N2400,(13,10,"Pi DC Power Switched ON")		'Echo Pi State
   time = 0									'Reset the Time 
  endif
 endif  

loop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Post_Data:
 serout 1,T2400,(":0",b8,44,b9,44,#w5,44,#b13,13,10)			
 'Tx Data packet to Pi
 serout 0,N2400,(13,10,"Post Data to Pi = ",":0",b8,44,b9,44,#w5,44,#b13)
 'Echo Local Data to Programming Lead
 nap 5					
 'Picaxe > Pi > Python Cayenne limit data upload rate
 return

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
RF_RX:
 serin 3,N2400,(":0",b8),b9,b10,b11,b12	'Listen for ":0X" and read in following 4 bytes
							'b9=Channel, b10 and b11 Lo and Hi byte data, b12 CSum
Check_Sum:
 b13 = b8 XOR b9 XOR b10 XOR b11 XOR b12	'Check data test using XOR
 serout 0,N2400,(13,10,"ASK_RF_Rx:",9,":0",b8,b9,32,#w5,32,#b12,32,#b13,9,9,#pin2)
 'Echo check sum result to programming lead to see what is happeing

Filter_Data_Packet: 
 if b13 = 0 then 		   		'If CSum result = GOOD = a zero then...
  gosub Post_Data				'Forward all data > Pi > Cayenne www
  inc b21					'Inc Good Data QoS counter
 else						'Otherwise if Bad_Rx_Data: 
  inc b22					'Inc Bad QoS counter
 endif
 return
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

mVcc:                'CalibADC10 Picaxe Vcc mVolt Precisewise Linear Interpolator    
 calibadc10 w10        'Read a 1.024 volts internal refference voltage.  w10 = 25500 / w10                 'Rough calc b3 to 10'ths of a volt
 w10 = w10 MAX 420    'Set Max range 420 = ~ 2500 mV
 w10 = w10 MIN 165    'Set MIN range 165 = ~ 6.5 volts
 b22 = 420 - w10        'Calculate which EEPROM step value
 w12 = 2492            'Load Minimum range mV
 for b0 = 0 to b22    'Look up and ADD step values
  read b0,b23        'Lookup EEPROM step value
  w12 = w12 + b23        'Compound ADD to Minimum range mV
 next                'Until maximum calibadc10 step reached
 serout 0,N2400,(13,10,"Battery Volts = ",#w12)		'Echo battery Voltage
 return
 
Data (0,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16,17,17,17,17,17,17,17,18,18,18,18,18,18,18,19,19,19,19,19,19,20,20,20,20,20,20,21,21,21,21,21,22,22,22,22,22,23,23,23,23,23,24,24,24,24,25,25,25,25,26,26,26,26,27,27,27,27,28,28,28,29,29,29,29,30,30,30,31,31,31,32,32,33,33,33,34,34,34,35,35,36,36,36,37,37,38,38)

Bat_Voltage:                'This is a method to infer battery voltage
 calibadc10 w1                'Read a 1.024 volts internal refference voltage.  w10 = 25500 / w10                 'Rough calc b3 to 10'ths of a volt
 w3 = 262 - w1 * 15 + 4000        'Approx 15 mV per calibadc10 count @ 4 Volts

