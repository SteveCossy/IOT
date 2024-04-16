# Ping all nodes on the SfTI network (TI Board interface) once
#
# Steve Cosgrove 10 April 2024    Modified from oncePing.sh to reduce output and place it on Jetson USB storage 17 April
#
# This file should be downloaded to ~/IPtools/
# The following lines should be used to run this script every 30 minutes
# sudo crontab -e
# ... add this line to the end of the existing crontab file:
# */30 * * * * /home/jetson/IPtools/fieldPing.sh

outputUSB=/media/jetson/KINGSTON
outputFolder=/networking
outputFile=pingTest

outputPath=$outputUSB$outputFolder$outputFile

if [ -d $outputUSB ]
then
    echo USB device not found
else

    # Create a new folder if necessary.  No error message if it doesn't work
    mkdir -p $outputUSB$outputFolder

    echo -n Connectivity check from `hostname` at `date` >> $outputPath

    for node in $(seq 1 10) ;
       do
       ping6 -c 1 -w 3 n$node >/dev/null
       if [ $? -eq 0 ]
          then RESULT=works
          else RESULT=failed
       fi
       echo -n Node $node: $RESULT ;

    done
echo

fi
