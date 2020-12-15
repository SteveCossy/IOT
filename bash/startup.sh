# Script to run at every boot

# Turn off hdmi
tvservice -o

# Name the traffic Log file with current date, time and seconds
LogFileNet=/home/pi/trafficlogs/skinkPiNet-`date +%y%m%d%H%M%S`.log

# Keep a status log for each day only
StatusLog=/home/pi/trafficlogs/skinkpi-`date +%y%m%d`.log

# Log the Read Once Python code with date, time, seconds
ReadLog=/home/pi/trafficlogs/read_once-`date +%y%m%d%H%M%S`.log
ReadErr=/home/pi/trafficlogs/read_err-`date +%y%m%d%H%M%S`.log

PINGTARGET=mydevices.com

# Track network traffic in background
sudo tcpdump > $LogFileNet &

# Note that we have started
echo `date +%y%m%d%H%M` New session started \*\*\* >> $StatusLog
# Check whether Cayenne routine is running
ps -ef | grep myDevices | grep -v grep >> $StatusLog

WAITING=true
while $WAITING
do
    if ping $PINGTARGET -c 1 >\dev\nul 2>\$ReadErr
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

sleep 120 # give myself another two minutes to log in if I want to!
userList=`users`

if [ ${#userList} != "0" ]  # More than zero users logged in
then
	sudo echo `date +%y%m%d%H%M` $userList Logged in - aborting script  >> $StatusLog
else
	sudo echo `date +%y%m%d%H%M` Shutting down >> $StatusLog
	sudo poweroff
fi
