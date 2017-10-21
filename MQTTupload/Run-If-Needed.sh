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

OUTFILE=/home/pi/Run-At-Reboot-Text
OUTERROR=/home/pi/Run-At-Reboot-Error
CHECKTEXT=MQTT3
CHECKFULPATH=/home/pi/IOT/MQTTupload/Serial_multi_MQTT3.py

# Check that only one CHECKTEXT is running.  Kill surplus copies!
if [ `ps -ef | grep -v grep | grep -c $CHECKTEXT` -gt 1 ]
then
	echo -n Multiple copies of $CHECKTEXT found: >>$OUTFILE
        date >>$OUTFILE
	pkill -f $CHECKFULPATH
fi


if [ `ps -ef | grep -v grep | grep -c $CHECKTEXT` -eq 0 ]
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
		if ping mydevices.com -c 1 >\dev\nul 2>\$OUTFILE
			then WAITING=false
		fi
		sleep 1
	done

	echo -n ping working     : >>$OUTFILE
	date >>$OUTFILE

	/usr/bin/python3 /home/pi/IOT/MQTTupload/Serial_multi_MQTT3.py >>$OUTFILE 2>>$OUTERROR &

else
	echo -n C- >>$OUTFILE
#	echo -n C- $CHECKTEXT: >>$OUTFILE
#        date >>$OUTFILE
fi
