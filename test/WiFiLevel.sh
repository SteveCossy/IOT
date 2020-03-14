# https://linux.die.net/man/8/iwconfig
# https://linuxize.com/post/bash-while-loop/
# /home/pi/IOT/test/WiFiLevel.sh Sunday-Open-Again | tee -a ~/wlan0-stats.log &


echo `date` - $1

while :
 do
 cat /proc/net/wireless | grep wlan0
 sleep 3
 done

