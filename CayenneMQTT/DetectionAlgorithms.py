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

def DetectErr(Temp, ErrThresh):
    global ErrorCount
    global PrevTemp

    ErrDetected = 0
    ErrThresh = int(ErrThresh)
    print('ErrThresh = ', ErrThresh)
    NegThresh = 0 - ErrThresh
    print('PrevTemp = ', PrevTemp)
    # The if statements check if the temperature varienmce is unreasonable
    if PrevTemp != 0:
        if (Temp - PrevTemp) > ErrThresh or (Temp - PrevTemp) < NegThresh: 
            print ('Error found')
            print('Temp = ', Temp, 'PrevTemp = ', PrevTemp)
            ErrorCount += 1
            ErrDetected = 1
        else:
            print('All good')
            PrevTemp = Temp
    elif Temp < 50:
        print('Temp under 50')
        PrevTemp = Temp
    else:
        print('Temp over 50')
        ErrorCount += 1
        ErrDetected = 1

    return ErrDetected
    
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
    
    return ErrorCount

def GetPrevTemp():
    # If an error is detected use this method rather than hold PrevTemp twice
    global PrevTemp

    return PrevTemp