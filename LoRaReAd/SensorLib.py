#!/usr/bin/env python
# https://stackoverflow.com/questions/1052589/how-can-i-parse-the-output-of-proc-net-dev-into-keyvalue-pairs-per-interface-u

ErrCount = 0 # Holds a count of the errors detected;
             # Make it readble by other things, perhaps displayed on Cayenne dashboard

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
    import toml
    global ErrCount

    PrevTemp = 0 # Holds previous temperature to compare it to new temp
    StartupChk = False # Holds a bool that should change once the sensor is actually reporting data
    # False by default to prevent the error detection from couting a false positive caused by expected behaviour when first plugging in a sensor

    device_folder = glob.glob('/sys/bus/w1/devices/28*')
    device_file = [device_folder[0] + '/w1_slave']
    # Add more code here and a link below to cope with multiple sensors

    tomlFile = GetThesholdFile()

    Postemp = toml.load(tomlFile)
    NegTemp = 0 - Postemp

    FilePath = open(device_file[0], 'r')
    LineOfData = FilePath.readlines()
    FilePath.close()

    Equals_Pos = LineOfData[1].find('t=')
    Temp = float(LineOfData[1][Equals_Pos+2:])/1000

    print('Startup = ', StartupChk)
    print('PrevTemp = ', PrevTemp)
    print('NewTemp = ', Temp)
    if StartupChk == True:
    # If the stratupChk is True, the method has been called at least once
        
        # The if statements check if the temperature varienmce is unreasonable
        if (Temp - PrevTemp) > Postemp or (Temp - PrevTemp) < NegTemp: # A change in 10 degrees should be enough 
            Temp = PrevTemp
            ErrCount += 1 # Changes the newly reported temp to the last accepted temp

        else:
            PrevTemp = Temp # Changes the to be the next accepted temp

    else:
        if Temp < 500: # 50 seems a reasonable temp, the spikes are supposed to be 100-200 degrees
            StartupChk = True
        else: # The spikes tend to be only one reading, so this should catch it
            Temp = 0
            ErrCount += 1

# debug    print( LineOfData[0], Temp, "'", LineOfData[0].strip()[-3:], "'" )

    if LineOfData[0].strip()[-3:] != 'YES' :
    # didn't sucessfully read temperature
        Temp = 0

    return Temp

def DetectPeng(DetectThresh):
    OldAvg = 0
    NewAvg = TempAvg()
    IsPenguin = 0

    if OldAvg != 0: # If there haven't been enough cycles to collect the necessary data just skip this
                    # Can also happen if there are a lot of errors, but that is what error detection is for
        AvgDiff = NewAvg - OldAvg
        if AvgDiff > DetectThresh: # Need to double check what threshold would work
            IsPenguin = 1

    OldAvg = NewAvg
    return IsPenguin

def TempAvg():
    TempHistory = []

    NewTemp = ReadTemp()

    if len(TempHistory) < 5:
        TempHistory.append(NewTemp)
        ReturnValue

    else:
        for T in TempHistory:
            TempHistory[T] = TempHistory[T + 1]
            
            if TempHistory.index(T) == (TempHistory.len() - 1):
                TempHistory[T] = NewTemp
                break
    
    ReturnValue = sum(TempHistory) / len(TempHistory)
    return ReturnValue

def GetErrCount():
    global ErrCount

    return ErrCount

if __name__ == '__main__':
    Result = GetWirelessStats()
    print( Result )


def GetThesholdFile():
    import os

    HomeDir  = os.environ['HOME']
  
    tomlFile = HomeDir+'/thresholds.txt'

    return tomlFile