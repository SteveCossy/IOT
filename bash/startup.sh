# Turn off hdmi to save power
tvservice -o

# Track network traffic in background
sudo tcpdump > /home/pi/trafficlogs/skinkpi-`date +%y%m%d%H%M`.log &

#Things are started - stop in four minutes
sleep 240
sudo poweroff

