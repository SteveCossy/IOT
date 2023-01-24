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
        echo No HC-06 devices found!
        ;;
    1)
        # Found exactly one device.  Get its MAC address
        MAC=`bluetoothctl devices | grep HC-06 | cut -d ' ' -f2`
        
        # Bind BT device to a file if not done already
        DEVICES=`ls /dev/rfcomm0 2>nul | wc `
        if [ $DEVICES = '0' ]
        then
            sudo rfcomm bind rfcomm0 $MAC
        else
            echo Device file found
        fi
        
        minicom -b 9600 -o -D /dev/rfcomm0 -C $LOG
        
        echo One HC-06 device found and used.
        ;;
    *)
        echo $COUNT \(more than one\) HC-06 devices found!
        ;;
esac

echo $MSG
