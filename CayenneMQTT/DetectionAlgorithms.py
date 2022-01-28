"""
    This script contains the algorithms used to detect erros and the possible presence of penguins based on temperature.
"""

ErrorCount = 0 # A global variable to be accessed by more than one mthod within this file
PrevTemp = 0 # A global vairable to give the variable some permanace, rather than have it redefined each time the DetectErr mthod is called

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
    global PrevTemp

    DetectThresh = int(DetectThresh)

    StartupChk = False # Holds a bool that should change once the sensor is actually reporting data
    # False by default to prevent the error detection from couting a false positive caused by expected behaviour when first plugging in a sensor
    NegThresh = 0 - DetectThresh
    print('PrevTemp = ', PrevTemp)
    # The if statements check if the temperature varienmce is unreasonable
    if (Temp - PrevTemp) < DetectThresh or (Temp - PrevTemp) > NegThresh:
        print('Temp = ', Temp, 'PrevTemp = ', PrevTemp)
        Temp = PrevTemp # Changes the newly reported temp to the last accepted temp
        ErrorCount += 1
    else:
        PrevTemp = Temp
    
def TempAvg(Temp):
    # Calculates the average of the last 5 temperatures
    # At Time of writing, it is only used by DetectPeng, 
    # but could be used for other purpose, and so is kept serparate
    TempHistory = []

    NewTemp = Temp

    if len(TempHistory) < 5:
        TempHistory.append(NewTemp)
    else:
        for T in TempHistory:
            TempHistory[T] = TempHistory[T + 1]
            
            if TempHistory.index(T) == (TempHistory.len() - 1):
                TempHistory[T] = NewTemp
                break
    
    ReturnValue = sum(TempHistory) / len(TempHistory)
    return ReturnValue

def GetErrorCount():
    global ErrorCount

    ErrorCount

    return ErrorCount