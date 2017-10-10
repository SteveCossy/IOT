OUTFILE=/home/pi/Run-At-Reboot-Text
OUTERROR=/home/pi/Run-At-Reboot-Error

echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
echo -n About to start at: >>$OUTFILE
date >>$OUTFILE

# Wait for webiopi to get started
while [ `ps -ef | grep -v grep | grep -c webiopi` -eq 1 ] ; do sleep 1 ; done

echo -n webiopi running: >>$OUTFILE
date >>$OUTFILE

# Wait till networking is working
WAITING=true

while $WAITING do
	if ping mydevices.com -c 1 >\dev\nul 2>\$OUTFILE
		then WAITING=false
	fi
	sleep 1
done

echo -n ping working: >>$OUTFILE
date >>$OUTFILE

/usr/bin/python3 /home/pi/IOT/MQTTupload/Serial_multi_MQTT3.py >>$OUTFILE 2>>$OUTERROR 


