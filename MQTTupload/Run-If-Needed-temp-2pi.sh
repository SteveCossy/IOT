#!/bin/bash
# Bash script to start and check running of the python script reading two temperature sensors connected directly to a Pi
# This script based on Run-If-Needed-home.sh, 09 May 2018
# Requires the following crontab entry (not run with sudo):
# crontab -e
# * * * * * /home/pi/IOT/MQTTupload/Run-If-Needed.sh
#
# Steve - 18 October 2017
# sensor-base modifications 25 January 2018

OUTFILE=/home/pi/Run-At-Reboot-Text
OUTERROR=/home/pi/Run-At-Reboot-Error

# CHECKONE=send_temps

CHECKTWO=send_email.py
CHECKTHREE=Bus_to_MQTT.py

FULPATHTWO=/home/pi/IOT/readsensors/send_email.py
FULPATHTHREE=/home/pi/IOT/MQTTupload/Bus_to_MQTT.py

PINGTARGET=bbc.com

# Check that only one CHECKTWO is running.  Kill surplus copies!
if [ `ps -ef | grep -v grep | grep -c $CHECKTWO` -gt 1 ]
then
	echo -n Multiple copies of $CHECKTWO found: >>$OUTFILE
        date >>$OUTFILE
	pkill -f $FULPATHTWO
fi
# Check that only one CHECKTHREE is running.  Kill surplus copies!
if [ `ps -ef | grep -v grep | grep -c $CHECKTHREE` -gt 1 ]
then
	echo -n Multiple copies of $CHECKTHREE found: >>$OUTFILE
        date >>$OUTFILE
	pkill -f $FULPATHTHREE
fi

# Check network connectivity, and document check, if program not running
if [ `ps -ef | grep -v grep | grep -c $CHECKTWO` -eq 0 ]
then
	# Wait till networking is working
#	WAITING=true
#	while $WAITING
#	do
#        	if ping $PINGTARGET -c 1 >\dev\nul 2>\$OUTFILE
#                	then WAITING=false
#	        fi
#        	sleep 1
#	done

#	echo -n ping working     : >>$OUTFILE
#	date >>$OUTFILE

# Wait for CHECKONE to be running
# while [ `ps -ef | grep -v grep | grep -c $CHECKONE` -eq 0 ]
# do
#	echo -n Waiting for $CHECKONE at: >>$OUTFILE
#        date >>$OUTFILE
#	sleep 5
# done

        echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
        echo -n About to restart $CHECKTWO: >>$OUTFILE
        date >>$OUTFILE

        /usr/bin/python3 $FULPATHTWO >>$OUTFILE 2>>$OUTERROR &

else
        echo -n 2- >>$OUTFILE
fi



if [ `ps -ef | grep -v grep | grep -c $CHECKTHREE` -eq 0 ]
then
	echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
 	echo -n About to restart $CHECKTHREE: >>$OUTFILE
 	date >>$OUTFILE

 	/usr/bin/python3 $FULPATHTHREE >>$OUTFILE 2>>$OUTERROR &

# else
	echo -n 3- >>$OUTFILE
#	echo -n C- $CHECKTWO: >>$OUTFILE
#       date >>$OUTFILE
fi
