#!/bin/bash
# Bash script to start and check running of the python script sending data to MQTT server (Cayanne)
# Replaced a cron job that used to run @reboot.  Advantages:
#   - more elegant solution - one file that serves two purposes so easier to maintain
#   - runs as a regular user (pi), not root, which improves security
# Requires the following crontab entry (not run with sudo):
# crontab -e
# * * * * * /home/pi/IOT/MQTTupload/Run-If-Needed.sh
#
# Steve - 18 October 2017
# sensor-base modifications 25 January 2018

OUTFILE=/home/pi/Run-At-Reboot-Text
OUTERROR=/home/pi/Run-At-Reboot-Error

CHECKONE='mosquitto '

CHECKTWO=mosquitto_csv_all.py

FULPATH=/home/pi/IOT/MQTTupload/mosquitto_csv_all.py
PINGTARGET=iotdata.kiwi

# Check that only one CHECKTWO is running.  Kill surplus copies!
if [ `ps -ef | grep -v grep | grep -c $CHECKTWO` -gt 1 ]
then
	echo -n Multiple copies of $CHECKTWO found: >>$OUTFILE
        date >>$OUTFILE
	pkill -f $FULPATH
fi

# Wait for CHECKONE to be running
while [ `ps -ef | grep -v grep | grep -c $CHECKONE` -eq 0 ]
do
	echo -n Waiting for $CHECKONE at: >>$OUTFILE
        date >>$OUTFILE
	sleep 5
done



if [ `ps -ef | grep -v grep | grep -c $CHECKTWO` -eq 0 ]
then
	echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
	echo -n About to restart at: >>$OUTFILE
	date >>$OUTFILE

	# DON'T  Wait for webiopi to get started
#	while [ `ps -ef | grep -v grep | grep -c webiopi` -eq 0 ] ; do sleep 1 ; done

#	echo -n webiopi running  : >>$OUTFILE
#	date >>$OUTFILE

	# Wait till networking is working
	WAITING=true

	while $WAITING
	do
		if ping $PINGTARGET -c 1 >\dev\nul 2>\$OUTFILE
			then WAITING=false
		fi
		sleep 1
	done

	echo -n ping working     : >>$OUTFILE
	date >>$OUTFILE

	/usr/bin/python3 $FULPATH >>$OUTFILE 2>>$OUTERROR &

else
	echo -n C- >>$OUTFILE
#	echo -n C- $CHECKTWO: >>$OUTFILE
#        date >>$OUTFILE
fi
