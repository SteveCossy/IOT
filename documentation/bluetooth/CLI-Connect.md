# Connecting to a serial Bluetooth Device from Command line
... well, not connect actually ... don't need to.

Based on: https://raspberrypi.stackexchange.com/questions/82173/failed-to-connect-org-bluez-error-notavailable-error

## bluetoothctl part

```
pi@raspberrypi:~ $ sudo bluetoothctl
Agent registered
[bluetooth]# scan on
Discovery started
[bluetooth]# trust 00:18:E4:34:E7:08
[CHG] Device 00:18:E4:34:E7:08 Trusted: yes
Changing 00:18:E4:34:E7:08 trust succeeded
[bluetooth]# pair 00:18:E4:34:E7:08
Attempting to pair with 00:18:E4:34:E7:08
[CHG] Device 00:18:E4:34:E7:08 Connected: yes
Request PIN code
[agent] Enter PIN code: 1234
[CHG] Device 00:18:E4:34:E7:08 UUIDs: 00001101-0000-1000-8000-00805f9b34fb
[CHG] Device 00:18:E4:34:E7:08 ServicesResolved: yes
[CHG] Device 00:18:E4:34:E7:08 Paired: yes
Pairing successful
[CHG] Device 00:18:E4:34:E7:08 ServicesResolved: no
[CHG] Device 00:18:E4:34:E7:08 Connected: no
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -87
```
[The complete scrollback from which I learned the above is here](https://github.com/SteveCossy/IOT/blob/21f95c2ee71219f6d6e71855a51a673d4e85a63f/documentation/bluetooth/zCLI-001.md)

## Connection part

Open a new terminal, and connect with *minicom*.
```

```
Obviously, there is a baud rate problem.  I tried starting minicom at 2400 baud, but that made no difference.  Suspect problem is mismatched baud rate between the humidity sensor and Bluetooth module.

