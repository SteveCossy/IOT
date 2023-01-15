# Connecting to a serial Bluetooth Device from Command line
... well, not 'connect' in the Bluetooth sense ... don't need to.

Based on: https://raspberrypi.stackexchange.com/questions/82173/failed-to-connect-org-bluez-error-notavailable-error

### Quick Summary

#### Existing Device

pi@raspberrypi:~ $ `bluetoothctl devices`<br>
pi@raspberrypi:~ $ `bluetoothctl info 00:18:E4:34:E7:08`<br>

    Device 00:18:E4:34:E7:08 (public)
        Name: HC-06
        Alias: HC-06
        Class: 0x00001f00
        Paired: yes

pi@raspberrypi:~ $ `sudo rfcomm bind rfcomm0 00:18:E4:34:E7:08`<br>
#check that the serial port as been created as refcomm0<br>
pi@raspberrypi:~ $ `ls -l /dev/rfcom*`<br>
`crw-rw---- 1 root dialout 216,   0 Jan 15 16:34 /dev/rfcomm0`<br>
pi@raspberrypi:~ $ `minicom -b 2400 -o -D /dev/rfcomm0`<br>


#### New Device

pi@raspberrypi:~ $ `bluetoothctl`<br>
[bluetooth]# `scan on`<br>
[NEW] Device 00:18:E4:34:E7:08 Name: HC-06<br>
[bluetooth]# `trust 00:18:E4:34:E7:08`<br>
[bluetooth]# `pair 00:18:E4:34:E7:08`<br>
&nbsp;&nbsp;Attempting to pair with 00:18:E4:34:E7:08<br>
&nbsp;&nbsp;[CHG] Device 00:18:E4:34:E7:08 Connected: yes<br>
&nbsp;&nbsp;Request PIN code<br>
&nbsp;&nbsp;[agent] Enter PIN code: `1234`<br>
[bluetooth]# `quit`<br>
pi@raspberrypi:~ $ `sudo rfcomm bind rfcomm0 00:18:E4:34:E7:08`<br>
#check that the serial port as been created as refcomm0<br>
pi@raspberrypi:~ $ `ls -l /dev/rfcom*`<br>
`crw-rw---- 1 root dialout 216,   0 Jan 15 16:34 /dev/rfcomm0`<br>
pi@raspberrypi:~ $ `minicom -b 2400 -o -D /dev/rfcomm0`<br>


### bluetoothctl part

```
pi@raspberrypi:~ $ bluetoothctl
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
quit
sudo rfcomm bind rfcomm0 00:18:E4:34:E7:08
```
[The complete scrollback from which I learned the above is here](https://github.com/SteveCossy/IOT/blob/21f95c2ee71219f6d6e71855a51a673d4e85a63f/documentation/bluetooth/zCLI-001.md)

## Connection part

Open a new terminal, and connect with *minicom*.
```
minicom -b 9600 -o -D /dev/rfcomm0

Welcome to minicom 2.7.1

OPTIONS: I18n
Compiled on Aug 13 2017, 15:25:34.
Port /dev/rfcomm0, 21:51:55

Press CTRL-A Z for help on special keys

�ø�ø�����ø�øø��ø������ø�øø�ø�øøø�����ø�øøø�ø���øø�������ø�ø�����ø�øø���ø���

```
Obviously, there is a baud rate problem.  I tried starting minicom at 2400 baud, but that made no difference.  Suspect problem is mismatched baud rate between the PICAXE and Bluetooth module.

## References
https://raspberrypi.stackexchange.com/questions/82173/failed-to-connect-org-bluez-error-notavailable-error
https://docs.github.com/en/get-started/using-github/keyboard-shortcuts#source-code-editing
https://ubuntu.com/core/docs/bluez/reference/pairing/introduction
https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/#listing-paired-devices-with-bluetoothctl
