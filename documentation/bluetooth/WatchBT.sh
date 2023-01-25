# Watch Bluetooth
# Steve Cosgrove 25 January 2023
# Find HC-06 client and display BT Serial text coming from it
# Please let me know how you get on using this!

# To use:
#	Put contents of this document into a text file called WatchBT.sh
#	Change the location of the log file to something that works for you
#	Make the file executable # chmod a+x WatchBT.sh
#	Run the file ./WatchBT.sh

# Set where we want to put log files:
LOG=/home/pi/IOT/documentation/bluetooth/zBT-Cap.log

# Check how many devices we can find:
COUNT=`bluetoothctl devices | grep -c HC-06`
case $COUNT in
    0)
        echo No HC-06 devices paired!
        ;;
    1)
        # Found exactly one device.  Get its MAC address
        MAC=`bluetoothctl devices | grep HC-06 | cut -d ' ' -f2`
        
        # Bind BT device to a file if not done already
        DEVICES=`ls /dev/rfcomm0 2>nul | wc -l `
        if [ $DEVICES = '0' ]
        then
            sudo rfcomm bind rfcomm0 $MAC
        else
            echo Device file found
        fi
        
        # Put the current date & time in a new line of the log file
        echo >> $LOG
        echo >> $LOG
        date >> $LOG
        
        minicom -b 9600 -o -D /dev/rfcomm0 -C $LOG
#        echo DEBUG - ran minicom
        
        echo One HC-06 device is paired.  Connection attempted.
        ;;
    *)
        echo $COUNT \(more than one\) HC-06 devices found!
        ;;
esac

echo $MSG

# Device must be paired before use - These command lines should help with pairing
#
# pi@raspberrypi:~ $ bluetoothctl
# Agent registered
# [bluetooth]# scan on
# Discovery started
# [bluetooth]# trust 00:18:E4:34:E7:08
# [CHG] Device 00:18:E4:34:E7:08 Trusted: yes
# Changing 00:18:E4:34:E7:08 trust succeeded
# [bluetooth]# pair 00:18:E4:34:E7:08
# Attempting to pair with 00:18:E4:34:E7:08
# [CHG] Device 00:18:E4:34:E7:08 Connected: yes
# Request PIN code
# [agent] Enter PIN code: 1234
# [CHG] Device 00:18:E4:34:E7:08 UUIDs: 00001101-0000-1000-8000-00805f9b34fb
# [CHG] Device 00:18:E4:34:E7:08 ServicesResolved: yes
# [CHG] Device 00:18:E4:34:E7:08 Paired: yes
# Pairing successful

# Update this file on GitHub
# cd /home/pi/IOT/ && git add /home/pi/IOT/documentation/bluetooth/* && git commit -m "Updating BT files" && git push

# screen command can run this in background
# sudo apt-get install screen
# screen

# If Pi session crashes, use this command to reconect:
# screen -r
# Run this file entirely in the background
# screen -de^tt -m /home/pi/IOT/documentation/bluetooth/WatchBT.sh
# then
#	screen -r to reconnect to the screen and see what it happening
#	^td to detach from screen and return to Linux command prompt