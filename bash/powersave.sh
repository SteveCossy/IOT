# Turn off anything we are not using.
# Steve Cosgrove, 22 November 2020
#
# https://learn.pi-supply.com/make/how-to-save-power-on-your-raspberry-pi/#turn-off-hdmi-output
# Turn OFF HDMI output
sudo /opt/vc/bin/tvservice -o
# Turn ON HDMI output
# sudo /opt/vc/bin/tvservice -p
#
# edit the /boot/config.txt file
#
# https://learn.pi-supply.com/make/how-to-save-power-on-your-raspberry-pi/#disable-wi-fi-bluetooth
# dtoverlay=pi3-disable-wifi
# dtoverlay=pi3-disable-bt
#
# https://learn.pi-supply.com/make/how-to-save-power-on-your-raspberry-pi/#disable-on-board-leds
# dtparam=act_led_trigger=none
# dtparam=act_led_activelow=on

