OUTFILE=/home/pi/Run-At-Reboot-Text
OUTERROR=/home/pi/Run-At-Reboot-Error

echo \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* >>$OUTFILE
echo -n About to start at: >>$OUTFILE
date >>$OUTFILE

sleep 120

/usr/bin/python3 /home/pi/IOT/MQTTupload/Serial_multi_MQTT3.py >>$OUTFILE 2>>$OUTERROR 


