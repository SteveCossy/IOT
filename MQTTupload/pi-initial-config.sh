# bash script to run commands to set up Pi for Caynne comms.
# October 2017
# References
# https://hallard.me/enable-serial-port-on-raspberry-pi/
# http://www.instructables.com/id/Read-and-write-from-serial-port-with-Raspberry-Pi/
# https://www.raspberrypi.org/forums/viewtopic.php?t=21110
# https://www.google.co.nz/search?newwindow=1&q=raspberry+pi+enable+serial+port&oq=raspberry+pi+enable+serial+&gs_l=psy-ab.1.0.0l2j0i22i30k1l8.242195.244343.0.246859.14.10.0.0.0.0.340.1216.2-1j3.4.0....0...1.1.64.psy-ab..10.4.1216...0i20i263k1.0.ZA6-Ui4858Y
# https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-linux
# https://help.github.com/articles/checking-for-existing-ssh-keys/
# https://help.github.com/articles/connecting-to-github-with-ssh/
# https://help.github.com/articles/cloning-a-repository/
# https://mydevices.com/cayenne/docs/bring-your-own-thing-api/#cayenne-mqtt-api-libraries
# https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=7192&
# http://www.restapitutorial.com/lessons/whatisrest.html
# https://linux.die.net/man/1/nohup
# https://stackoverflow.com/questions/10408816/how-do-i-use-the-nohup-command-without-getting-nohup-out
# http://raspberrypihobbyist.blogspot.co.nz/2012/08/raspberry-pi-serial-port.html
# 
# Set startup option to boot to CLI
sudo ln -s /lib/systemd/system/multi-user.target /etc/systemd/system/default.target
#
sudo raspi-config
# Change: locale to en-NZ-UT8
#   Change Timezone to Pacific=>Auckland
#   Expand the firesystem
#   Would really perfer to do the above at command linesudo apt-get update

#   Reboot at this point to expand the filesystem!

# Update local software records, and upgrade software that has changed since image was created
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install screen
# Download and install the Cayenne Python tools
wget https://cayenne.mydevices.com/dl/rpi_uh0j8dymeg.sh
sudo bash rpi_uh0j8dymeg.sh -v
sudo pip3 install cayenne-mqtt
sudo pip3 install paho-mqtt

# Stop the serial port being set up use as a console
sudo nano /boot/cmdline.txt
#   remove the two options referring to the serial port
#   http://raspberrypihobbyist.blogspot.co.nz/2012/08/raspberry-pi-serial-port.html

# Set up git and download current version of the project
git config --global user.email "steve@rata.co.nz"
git config --global user.name "Steve"
ssh-keygen -t rsa -b 4096 -C "steve@rata.co.nz"
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
# copy key and paste it into github
git clone git@github.com:SteveCossy/IOT.git
# cat IOT/MQTTupload/Run-At-Reboot.sh

# ready to run the current code!
sudo /usr/bin/python3 /home/pi/IOT/MQTTupload/Serial_multi_MQTT3.py
