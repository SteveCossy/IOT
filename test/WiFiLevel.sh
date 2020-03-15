# https://linux.die.net/man/8/iwconfig
# https://linuxize.com/post/bash-while-loop/
# /home/pi/IOT/test/WiFiLevel.sh Sunday-Open-Again | tee -a ~/wlan0-stats.log &
# while : ; do cat /proc/net/wireless ; sleep ; done

if [ -z "$2" ]
then
      export Pause=15
else
      export Pause=$2
fi

echo `date` - $1

while :
 do
 cat /proc/net/wireless | grep wlan
 sleep $Pause
 done

