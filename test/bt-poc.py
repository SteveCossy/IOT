# Bluetooth Proof of Concept
# Steve Cosgrove 19 Jan 2023
# Need to run   $ pip3 install pydbus

# based on https://ukbaz.github.io/howto/bluetooth_overview.html
# import pydbus
import socket

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect(('00:18:E4:34:E7:08', 1))

print (s.recv(1024))


