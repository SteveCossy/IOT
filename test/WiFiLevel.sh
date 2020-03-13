# https://linux.die.net/man/8/iwconfig
# https://linuxize.com/post/bash-while-loop/

echo `date` - $1

while :
 do
 cat /proc/net/wireless | grep wlan0
 sleep 3
 done

