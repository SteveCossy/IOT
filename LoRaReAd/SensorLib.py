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

def GetSerialData(CSVPath,ClientID,SerialDetails) :
    import struct
    import serial
    from MQTTUtils import DataError
    from MQTTUtils import Save2Cayenne
    from MQTTUtils import Save2CSV

    Eq = 	' = '
    CrLf =  '\r\n'
    Qt  =   '"'

    # Set up serial port values
    DRF126x =       (SerialDetails["ModuleType"] == "DRF126x")
    SERIAL_PORT =   SerialDetails["DeviceName"]
    BAUDRATE =      SerialDetails["BAUDrate"]
    
    # Define Cicadacom Data Header
    HEADIN = 	b':'b'0'

    with serial.Serial(SERIAL_PORT, BAUDRATE) as ser:
       Sync = ser.read_until(HEADIN)

       if not(Sync==HEADIN):
            print( "Extra Sync text!", Sync, "**************")
#            Save2Cayenne (client, 'Stat', 1, 1)
            Save2CSV (CSVPath, ClientID, 'Sync-Error', Sync)

       if DRF126x :
            PacketIn = ser.read(6)
            Device,Channel,Data,Cks,RSSI=struct.unpack("<ccHBB",PacketIn)
       else:
            PacketIn = ser.read(5)
            Device,Channel,Data,Cks=struct.unpack("<ccHB",PacketIn)
            RSSI = 0

       print( PacketIn, len(PacketIn), 'l' )

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
         "ClientID" : ClientID,
         "Error"    : PacketIn,
       }

#       raise Exception('Test exception at line 96 of SensorLib.py')
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


def ReadTemp():
#   A function that grabs the raw temp data from a single DS18B20

    import glob
    device_folder = glob.glob('/sys/bus/w1/devices/28*')
    device_file = [device_folder[0] + '/w1_slave']
    # Add more code here and a link below to cope with multiple sensors

    FilePath = open(device_file[0], 'r')
    LineOfData = FilePath.readlines()
    FilePath.close()

    Equals_Pos = LineOfData[1].find('t=')
    Temp = float(LineOfData[1][Equals_Pos+2:])/1000

# debug    print( LineOfData[0], Temp, "'", LineOfData[0].strip()[-3:], "'" )

    if LineOfData[0].strip()[-3:] != 'YES' :
    # didn't sucessfully read temperature
        Temp = 0

    return Temp


if __name__ == '__main__':
    Result = GetWirelessStats()
    print( Result )
