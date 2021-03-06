#!/usr/bin/env python
# from: https://pypi.org/project/pi-ina219/
# print formatting: https://www.w3schools.com/python/python_string_formatting.asp
#              and: https://stackoverflow.com/questions/2122385/dynamic-terminal-printing-with-python

# Command line detection
# pi@skinkpi3:~ $ file /dev/i2c-1
# /dev/i2c-1: character special (89/1)
# pi@skinkpi3:~ $ i2cdetect 1


from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.3


def read():
   ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
   ina.configure(ina.RANGE_16V)
   keepPrinting = True
   oneLineOutput = "Bus {busVolts:5.2f} V, {busCurrent:6.2f} mA. Power {Power:6.2f} mW. Shunt {ShuntVolts:7.0f} mV"

   while keepPrinting :
     try:
       print ( oneLineOutput.format \
	(busVolts = ina.voltage(), \
	 busCurrent = ina.current(), \
	 Power = ina.power(), \
	 ShuntVolts = ina.shunt_voltage() \
	), \
	end='\r' )
     except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print (e)
     except KeyboardInterrupt:
        print ()
        print ("Quitting")
        keepPrinting = False


   print()

#    print("Bus Voltage: %.3f V" % ina.voltage())
#    try:
#        print("Bus Current: %.3f mA" % ina.current())
#        print("Power: %.3f mW" % ina.power())
#        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
#    except DeviceRangeError as e:
#        # Current out of device range with specified shunt resistor
#        print(e)


if __name__ == "__main__":
    read()


