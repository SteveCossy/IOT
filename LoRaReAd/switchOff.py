# Force GPIO 14 low to tell an attached PicAxe to shut off power soon
from gpiozero import LED
import os #imports OS library for Shutdown control

# Based on https://gpiozero.readthedocs.io/en/stable/recipes.html
indicator = LED(14)
indicator.off()

os.system("sudo poweroff") #shut down the Pi -h is or -r will reset
