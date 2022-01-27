"""
    This script contains the algorithms used to detect erros and the possible presence of penguins based on temperature.
"""

import toml

ErrorCount = 0

# This method should detect a rise in temperature that could indicate the presence of a penguin
def DetectPeng(Temp, DetectThresh):
    OldAvg = 0
    NewAvg = TempAvg(Temp)
    IsPenguin = 0

    if OldAvg != 0: # If there haven't been enough cycles to collect the necessary data just skip this
                    # Can also happen if there are a lot of errors, but that is what error detection is for
        AvgDiff = NewAvg - OldAvg
        if AvgDiff > DetectThresh: # Need to double check what threshold would work
            IsPenguin = 1

    OldAvg = NewAvg
    return IsPenguin

def DetectErr(Temp, DetectThresh):
    global ErrorCount

    PrevTemp = 0 # Holds previous temperature to compare it to new temp
    StartupChk = False # Holds a bool that should change once the sensor is actually reporting data
    # False by default to prevent the error detection from couting a false positive caused by expected behaviour when first plugging in a sensor
    # The if statements check if the temperature varienmce is unreasonable
    if (Temp - PrevTemp) < Postemp or (Temp - PrevTemp) > NegTemp:
        Temp = PrevTemp # Changes the newly reported temp to the last accepted temp
        ErrCount += 1

def TempAvg(Temp):
    # Calculates the average of the last 5 temperatures
    # At Time of writing, it is only used by DetectPeng, 
    # but could be used for other purpose, and so is kept serparate
    TempHistory = []

    NewTemp = ReadTemp()

    if TempHistory.len() < 5:
        TempHistory.append(NewTemp)
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