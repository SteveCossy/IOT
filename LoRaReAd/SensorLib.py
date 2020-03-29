#!/usr/bin/env python
# https://stackoverflow.com/questions/1052589/how-can-i-parse-the-output-of-proc-net-dev-into-keyvalue-pairs-per-interface-u

def GetWirelessStats() :
    dev = open("/proc/net/wireless", "r").readlines()
    # was using /proc/net/dev
    header_line = dev[1].replace("tus","status")
    header_names = header_line[header_line.index("|")+1:] \
        .replace("|", " ").replace("22", " ") \
        .split()

#	print (header_names)

    RawValues={}
    for line in dev[2:]: # Need his line for multiple interfaces
#    line = dev[2] # For one interface, this will do
        intf = line[:line.index(":")].strip() # Interface is at the start of the line
        RawValues[intf] = [int(value) \
            for value in line[line.index(":")+1:].replace(".", " ").split()]

#	print ( intf,RawValues )

    Values={intf:{}}
    for i in range(len(header_names)) :
        Values[intf][header_names[i]] = RawValues[intf][i]
    #    print (header_names[i] , values[intf][i] )

#	for desired in ['link','level'] :
#	    print (desired, Values[intf][desired])
    return (Values)

def GetSerialData() :

    from MQTTUtils import PiSerial
    Eq	= 	' = '
    CrLf	= 	'\r\n'
    Qt	= 	'"'

    # Variables specfic to reading sensor data
    DRF126x = 	False # must be DRF127x
    # DRF126x = 	True
    HEADIN = 	b':'b'0'

    # Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
    #  and the details should be put into the file listed above.

    # Read the Cayenne configuration stuff into a dictionary
    ConfigDict = toml.load(ConfPathFile)
    CayenneParam = ConfigDict.get('cayenne')

    # Set up the serial port.
    if ('USB0' in PiSerial() ):
        SERIAL_PORT = "/dev/ttyUSB0"
    else:
        SERIAL_PORT = "/dev/serial0"
    #    SERIAL_PORT =  "/dev/ttyAMA0"
    # Default location of serial port on Pi models 3 and Zero
    #    SERIAL_PORT =   "/dev/ttyS0"

    BAUDRATE=2400
    # These values appear to be the defaults
    #    parity = serial.PARITY_NONE,
    #    stopbits = serial.STOPBITS_ONE,
    #    bytesize = serial.EIGHTBITS,

    try:
     while SerialListen:
       with serial.Serial(SERIAL_PORT, BAUDRATE) as ser:
          Sync = ser.read_until(HEADIN)

          if not(Sync==HEADIN):
              print( "Extra Sync text!", Sync, "**************")
              Save2Cayenne (client, 'Stat', 1, 1)
              Save2CSV (CSVPath, CayenneParam.get('CayClientID'), 'Sync-Error', Sync)

          PacketIn = ser.read(5)
          print( PacketIn, len(PacketIn), 'l' )

          Device,Channel,Data,Cks=struct.unpack("<ccHB",PacketIn)
          if DRF126x :
              RSSI = ser.read(1)
          else:
              RSSI = 0

    # Checksum processing
          CksTest = 0
          for byte in PacketIn[0:5]:
              CksTest = CksTest ^ byte
          print(Device, Channel, Data, Cks, "RSSI = ", RSSI)
          Channel = str(Channel,'ASCII')
          SerialData = {
            "Device"   : Device,
            "Channel"  : Channel,
            "Data"     : Data,
            "RSSI"     : RSSI,
            "Status"   : 1,
            "ClientID" : CayenneParam.get('CayClientID'),
            "Error"    : PacketIn,
          }

          if CksTest == 0:
              print( 'Checksum correct!')
          else:
              print( '"Huston - We have a problem!" *******************************' )
              SerialData = {
                "Status"  : 0,
              }
              DataError(Device , Channel, \
                  "Checksums (recv/calc): "+str(Cks)+"/"+str(CksTest), PacketIn)
          return (SerialData)
    except KeyboardInterrupt:
      print(' ')

    except:
      Message = 'Exception Reading LoRa Data'
      ProcessError(CSVPath, CayenneParam.get('CayClientID'), \
           client, LOG_FILE, Message)


if __name__ == '__main__':
    Result = GetWirelessStats()
    print( Result )
