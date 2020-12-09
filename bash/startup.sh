# Script to run at every boot

# Turn off hdmi
tvservice -o

# Name the Log file with current date and time
LogFileNet=/home/pi/trafficlogs/skinkpi-`date +%y%m%d%H%M`.log

# Keep a status log for each day only
StatusLog=/home/pi/trafficlogs/skinkpi-`date +%y%m%d`.log

# Keep a status log for each day only
ReadLog=/home/pi/trafficlogs/read_once-`date +%y%m%d%H%M`.log

# Track network traffic in background
sudo tcpdump > $LogFile &

# Note that we have started
sudo echo `date +%y%m%d%H%M` New session started \*\*\* >> $StatusLog
# Check whether Cayenne routine is running
ps -ef | grep myDevices | grep -v grep >> $StatusLog

# (don't) Wait two minutes, start Cayneene stuff, then put a note in the log file
# sleep 120

python3 /home/pi/IOT/readsensors/read_one_temp.py >> $ReadLog &

sudo echo `date +%y%m%d%H%M` Starting Cayneene routines >> $StatusLog
sudo service myDevices start

# Things are started - stop in some minutes
sleep 570
sudo echo `date +%y%m%d%H%M` Shutting down >> $StatusLog

sudo poweroff

