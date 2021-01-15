# Force GPIO 14 low to tell an attached PicAxe to shut off power soon
from gpiozero import LED
import os #imports OS library for Shutdown control
import time

# Based on https://gpiozero.readthedocs.io/en/stable/recipes.html
indicator = LED(14)
start_time = time.time()

# Take down GPIO 14 and keep it off for 5 seconds
while time.time() < (start_time+8):
   indicator.off()

os.system("sudo poweroff") #shut down the Pi -h is or -r will reset
