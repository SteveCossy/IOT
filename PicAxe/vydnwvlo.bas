'#Picaxe-08M2
'#Com 6
'Set com Port for programming and serial terminal monitoring
'#Terminal 4800
#Terminal 2400
'Directive to set the Serial Terminal ro 4800 Baud
#No_Data
'Directive to prevent data table download
DisableBOD
'Select uPower Sleep mode

TTL:
High 4							'Preset Pin 4 of picaxe to (inverted RS232) TTL Voltage  
wait 1

do								'Do this foreva

Input_Readings:

Read_Temperature:
 readtemp12 1,w1
 w1 = w1 * 10 / 16
 
'Read_ADC:
' readadc 1,w1
' w1 = w1								'Convert hi res thermistor * 10 / 4

Tx_Pi_Data: 
 b10 = "A"								'Set b10 Channel Unique Student / Channel / Data ID
 b11 = w1								'Get b11 data
 b12 = 0'b10 XOR b11						'Go Generate Local checkSum using XOR
 serout 0,N2400,(":01",44,b10,44,#b11,44,#b12,13,10)		'Tx data packet up programming lead terminal F8 Screen
 serout 4,T2400,(":01",44,b10,44,#b11,44,#b12,13,10)		'Tx Identical data Packet from pin4 to the Raspi Pie 
 gosub Clock

Tx_Pi_Time: 
 b10 = "B"
 b11 = time								'Generate a very crude 'UpTime counter 0 - 255
 b12 = 0'b10 XOR b11
 serout 0,N2400,(":01",44,b10,44,#b11,44,#b12,13,10)		'Tx data packet up programming lead terminal F8 Screen
 serout 4,T2400,(":01",44,b10,44,#b11,44,#b12,13,10)		'Tx Identical data Packet from pin4 to the Raspi Pie 
 gosub Clock

Tx_Pi_Random: 
 b10 = "C"
 random w2								'Randomise WORD Valriable w2
 b11 = w2								'Read lower byte of W2 into data byte b11
 b12 = 0'b10 XOR b11
 serout 0,N2400,(":01",44,b10,44,#b11,44,#b12,13,10)		'Tx data packet up programming lead terminal F8 Screen
 serout 4,T2400,(":01",44,b10,44,#b11,44,#b12,13,10)		'Tx Identical data Packet from pin4 to the Raspi Pie 
 gosub Clock

loop									'Play it again Sam.......

Clock:
w0 = time + 10
Tick:
serout 0,N2400,("Tick = ",#b0,9,#time,13,10)		'Tx data packet up programming lead terminal F8 Screen
wait 1
if time < w0 then Tick
return


