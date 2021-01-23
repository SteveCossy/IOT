#!/bin/bash
# Bash script to start and check running of the python script reading two temperature sensors connected directly to a Pi
# This script based on Run-If-Needed-home.sh, 09 May 2018
# Requires the following crontab entry (not run with sudo):
# crontab -e
# * * * * * /home/pi/IOT/MQTTupload/Run-If-Needed-ZIP.sh
#
# Steve - 18 October 2017
# ZIP modifications 30 October 2018
# Reincarnated to do pretty much the same thing 25 January 2020

LOGDIR=$HOME/logs
# LOGDIR=/tmp  # Testing in different folder
OUTFILE=$LOGDIR/Run-If-Needed-Text
OUTERROR=$LOGDIR/Run-If-Needed-Error
PINGTARGET=mydevices.com

CHECKONE=cayMQTT_to_csv.py
CHECKTWO=MQTTmultiRead.py

FULPATHONE=/home/cosste/IOT/CayenneMQTT/cayMQTT_to_csv.py
FULPATHTWO=/home/cosste/IOT/CayenneMQTT/MQTTmultiRead.py

if [ -d $LOGDIR ]
then
    echo "Directory already exists"
else
    mkdir $LOGDIR
fi

# Check that only one CHECKONE is running.  Kill surplus copies!
for VAR in ONE TWO ; do
        eval THISFILE=\${CHECK$VAR}
        eval THISPATH=\${FULPATH$VAR}
        echo Checking $THISFILE
        if [ `ps -ef | grep -v grep | grep -v sudo | grep -c $THISFILE` -gt 1 ]
        then
	        echo -n Multiple copies of $THISFILE found: >>$OUTFILE
                date >>$OUTFILE
	        pkill -f $THISPATH
        fi
done

# Wait till networking is working
WAITING=true
while $WAITING
do
      	if ping $PINGTARGET -c 1 >/dev/null 2>>$OUTFILE
               	then WAITING=false
        fi
       	sleep 1
done

for VAR in ONE TWO ; do
        eval THISFILE=\${CHECK$VAR}
        eval THISPATH=\${FULPATH$VAR}
        echo $THISPATH
        # Check network connectivity, and document check if program not running
        if [ `ps -ef | grep -v grep | grep -c $THISFILE` -eq 0 ]
        # if [ 0 != 0 ] # reduce output while debugging
        then
        #       network has come up, so record that, with date
	        echo -n ping working     : >>$OUTFILE
	        date >>$OUTFILE

        #       (re)start the Python script, making a big song and dance in the output file
                echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
                echo -n About to restart $THISFILE: >>$OUTFILE
                date >>$OUTFILE
        #       start the Python, sending regular text to OutFile, and any errors to OutError.
                /usr/bin/python3 $THISPATH >/dev/null 2>>$OUTERROR &
        #       >nul gets rid of all messages.  Can't output to a file because of Cayenne PUB lines
        else
        #       All is sweet with the world - add comforting text into OutFile
                echo -n $VAR >>$OUTFILE
        fi
done

