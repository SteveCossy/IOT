# Sort out symbols
# http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=0x&unicodeinhtml=hex
POWER3 = u'\xb3'
DEG = u'\xb0'  # utf code for degree
# ENCODING = 'UTF-8'
# print DEG


SENSOR_NODES = {
	'A' : [ 'Temp', 'Temperature', DEG, 'degrees celcius' ],
        'B' : [ 'Humid', 'Humidity', '%', '%' ],
        'C' : [ 'Rain', 'Rainfall', 'millimetres' ],
        'D' : [ 'BaroP', 'Barametric Pressure', 'hPa', 'hectopascal' ],
        'E' : [ 'Capacitance', 'Capacitance', 'F', 'farad' ],
        'F' : [ 'Wght', 'Weight', 'g', 'grammes' ],
        'G' : [ 'Light', 'Light', 'lx', 'lux' ],
        'H' : [ 'Density', 'Density (mass)', 'g/cm'+POWER3, 'grammes per cubic centimetre' ],
        'I' : [ 'NodeI', 'Node I sensor data', 'I', 'Units of node I' ],
        'J' : [ 'NodeJ', 'Node J sensor data', 'J', 'Units of node J' ],
                        }

for NODE, UNITS in SENSOR_NODES.iteritems():
	print NODE, ": '",  
	for UNIT in UNITS:
		print  UNIT, "'", 
	print 

print

for NODE in SENSOR_NODES:
	DETAILS = SENSOR_NODES.get(NODE)
#	print 'Node', NODE, 'measures: ' , SENSOR_NODES.get(NODE[2])
	print 'Node', NODE, 'measures: ' , DETAILS[1] ,
	print 'in: ' , DETAILS[2] 
	

#        print (swl , links)
#        for sw2 in links:
#		print (swl, links, sw2)
