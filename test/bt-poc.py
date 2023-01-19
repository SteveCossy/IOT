# Bluetooth Proof of Concept
# Steve Cosgrove 19 Jan 2023
# Need to run   $ pip3 install pydbus

# based on https://ukbaz.github.io/howto/bluetooth_overview.html
# import pydbus
import socket

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect(('00:18:E4:34:E7:08', 1))

Run_flag=True # Get the loop started

while Run_flag :
    try:  # catch a <CTRL C>
        out = s.recv(1024)
        print (out)
    except KeyboardInterrupt:
        Run_flag=False # Stop the loop


