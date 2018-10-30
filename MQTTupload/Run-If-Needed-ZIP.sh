#!/bin/bash
# Bash script to start and check running of the python script reading two temperature sensors connected directly to a Pi
# This script based on Run-If-Needed-home.sh, 09 May 2018
# Requires the following crontab entry (not run with sudo):
# crontab -e
# * * * * * /home/pi/IOT/MQTTupload/Run-If-Needed-ZIP.sh
#
# Steve - 18 October 2017
# ZIP modifications 30 October 2018

OUTFILE=$HOME/Run-At-Reboot-Text
OUTERROR=$HOME/Run-At-Reboot-Error
PINGTARGET=mydevices.com

CHECKONE=Serial_to_MQTT.py

FULPATHONE=/home/pi/Serial_to_MQTT.py

# Check that only one CHECKONE is running.  Kill surplus copies!
if [ `ps -ef | grep -v grep | grep -v sudo | grep -c $CHECKONE` -gt 1 ]
then
	echo -n Multiple copies of $CHECKONE found: >>$OUTFILE
        date >>$OUTFILE
	pkill -f $FULPATHONE
fi

# Check network connectivity, and document check if program not running
if [ `ps -ef | grep -v grep | grep -c $CHECKONE` -eq 0 ]
then
	# Wait till networking is working
	WAITING=true
  while $WAITING
  do
        	if ping $PINGTARGET -c 1 >/dev/null 2>>$OUTFILE
                	then WAITING=false
	        fi
        	sleep 1
	done
  # network has come up, so record that, with date
	echo -n ping working     : >>$OUTFILE
	date >>$OUTFILE

  # (re)start the Python script, making a big song and dance in the output file
  echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
  echo -n About to restart $CHECKONE: >>$OUTFILE
  date >>$OUTFILE
  # start the Python, sending regular text to OutFile, and any errors to OutError.
  /usr/bin/python $FULPATHONE >/dev/null 2>>$OUTERROR &
#  /usr/bin/python3 $FULPATHONE >>$OUTFILE 2>>$OUTERROR &  
#  /usr/bin/python runs Python 2.7.  Would be better to use Python 3 
#  >>nul gets rid of all messages.  Can't output to a file because of Cayenne PUB lines
else
  # All is sweet with the world (Python file 1, really) - add a comforting two bytes (1-) into OutFile
  echo -n 1- >>$OUTFILE
fi
