# Script to run at every boot

# Turn off hdmi
tvservice -o

# Seconds to wait for login after Python code has finished
LOGINWAIT=120

# Name the traffic Log file with current date, time and seconds
LogFileNet=/home/pi/trafficlogs/skinkPiNet-`date +%y%m%d%H%M%S`.log

# Keep a status log for each day only
StatusLog=/home/pi/trafficlogs/skinkpi-`date +%y%m%d`.log

# Log the Read Once Python code with date, time, seconds
ReadLog=/home/pi/trafficlogs/read_once-`date +%y%m%d%H%M%S`.log
ReadErr=/home/pi/trafficlogs/read_err-`date +%y%m%d%H%M%S`.log

PINGTARGETip=104.198.207.59
PINGTARGET=mydevices.com
# Note that we have started
echo `date +%y%m%d%H%M` New session started \*\*\* >> $StatusLog
# Check whether Cayenne routine is running
# ps -ef | grep myDevices | grep -v grep >> $StatusLog

# Debugging log files
# echo `date +%y%m%d%H%M` New session started \*\*\* >> $LogFileNet
# echo `date +%y%m%d%H%M` New session started \*\*\* >> $ReadLog
# echo `date +%y%m%d%H%M` New session started \*\*\* >> $ReadErr

# Track network traffic in background
# sudo tcpdump >> $LogFileNet &

WAITING=true
while $WAITING
do
    if ping $PINGTARGETip -c 1 >\dev\nul 2>$ReadErr
    then WAITING=false
    fi
    sleep 1
done
WAITING=true
while $WAITING
do
    if ping $PINGTARGET -c 1 >\dev\nul 2>$ReadErr
    then WAITING=false
    fi
    sleep 1
done
echo `date +%y%m%d%H%M%S` Network Found, starting Python \*\*\* >> $StatusLog

# (don't) Wait two minutes, start Cayeene stuff, then put a note in the log file
# sleep 120
# sudo echo `date +%y%m%d%H%M` Starting Cayenne stuff >> $StatusLog
# sudo service myDevices start

# sudo echo `date +%y%m%d%H%M` Starting Read One Python >> $StatusLog

python3 /home/pi/IOT/LoRaReAd/oneTempToMQTT.py > $ReadLog 2> $ReadErr

sleep $LOGINWAIT # give myself some more time to log in if I want to!
userList=`users`

if [ ${#userList} != "0" ]  # More than zero users logged in
then
	sudo echo `date +%y%m%d%H%M` $userList Logged in - aborting script  >> $StatusLog
else
	sudo echo `date +%y%m%d%H%M` Shutting down >> $StatusLog
#	sudo poweroff
	python3 /home/pi/IOT/bash/switchOff.py

fi
