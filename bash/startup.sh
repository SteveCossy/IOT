# Script to run at every boot

# Turn off hdmi
tvservice -o

# Name the traffic Log file with current date, time and seconds
LogFileNet=/home/pi/trafficlogs/skinkpi-`date +%y%m%d%H%M%S`.log

# Keep a status log for each day only
StatusLog=/home/pi/trafficlogs/skinkpi-`date +%y%m%d`.log

# Log the Read Once Python code with date, time, seconds
ReadLog=/home/pi/trafficlogs/read_once-`date +%y%m%d%H%M%S`.log

# Track network traffic in background
sudo tcpdump > $LogFile &

# Note that we have started
sudo echo `date +%y%m%d%H%M` New session started \*\*\* >> $StatusLog
# Check whether Cayenne routine is running
ps -ef | grep myDevices | grep -v grep >> $StatusLog

# (don't) Wait two minutes, start Cayneene stuff, then put a note in the log file
# sleep 120

sudo echo `date +%y%m%d%H%M` Starting Read One Python >> $StatusLog
# sudo service myDevices start

python3 /home/pi/IOT/readsensors/read_one_temp.py >> $ReadLog

userList=`users`

if [ ${#userList} != "0" ]  # More than zero users logged in
then
	sudo echo `date +%y%m%d%H%M` $userList Logged in - aborting script  >> $StatusLog
else
	sudo echo `date +%y%m%d%H%M` Shutting down >> $StatusLog
	sudo poweroff
fi
