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


if __name__ == '__main__':
    Result = GetWirelessStats()
    print( Result )
