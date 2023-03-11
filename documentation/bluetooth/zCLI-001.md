```
pi@192.168.80.228's password:
     ┌────────────────────────────────────────────────────────────────────┐
     │                         • MobaXterm 8.6 •                          │
     │            (SSH client, X-server and networking tools)             │
     │                                                                    │
     │ ➤ SSH session to pi@192.168.80.228                                 │
     │   • SSH compression : ✔                                            │
     │   • SSH-browser     : ✔                                            │
     │   • X11-forwarding  : ✔  (remote display is forwarded through SSH) │
     │   • DISPLAY         : ✔  (automatically set on remote server)      │
     │                                                                    │
     │ ➤ For more info, ctrl+click on help or visit our website           │
     └────────────────────────────────────────────────────────────────────┘

Linux raspberrypi 5.10.103-v7+ #1529 SMP Tue Mar 8 12:21:37 GMT 2022 armv7l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jan 14 21:13:01 2023

SSH is enabled and the default password for the 'pi' user has not been changed.
This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

pi@raspberrypi:~ $ sudo bluetoothctl
Agent registered
[bluetooth]# scan on
Discovery started
[CHG] Controller B8:27:EB:3B:0C:D4 Discovering: yes
[NEW] Device 4B:55:6C:D8:80:02 4B-55-6C-D8-80-02
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -76
[NEW] Device 00:18:E4:34:E7:08 00-18-E4-34-E7-08
[CHG] Device 00:18:E4:34:E7:08 LegacyPairing: no
[CHG] Device 00:18:E4:34:E7:08 Name: HC-06
[CHG] Device 00:18:E4:34:E7:08 Alias: HC-06
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -68
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -87
[CHG] Device 00:18:E4:34:E7:08 LegacyPairing: yes
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -79
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -87
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -78
[bluetooth]# pair 00:18:E4:34:E7:08
Attempting to pair with 00:18:E4:34:E7:08
Failed to pair: org.bluez.Error.ConnectionAttemptFailed
[NEW] Device 49:C9:0A:C8:2F:52 49-C9-0A-C8-2F-52
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -67
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -88
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -68
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -88
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -81
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -68
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -87
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -93
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -79
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -88
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -78
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -68
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -88
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -83
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -79
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
[bluetooth]# connect 00:18:E4:34:E7:08
Attempting to connect to 00:18:E4:34:E7:08
[CHG] Device 00:18:E4:34:E7:08 Connected: yes
[CHG] Device 00:18:E4:34:E7:08 ServicesResolved: yes
Failed to connect: org.bluez.Error.NotAvailable
[CHG] Device 00:18:E4:34:E7:08 ServicesResolved: no
[CHG] Device 00:18:E4:34:E7:08 Connected: no
[CHG] Device 4B:55:6C:D8:80:02 RSSI: -77
[NEW] Device 61:24:0C:EA:AA:FC 61-24-0C-EA-AA-FC
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -69
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -77
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -87
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -75
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -88
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -93
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -79
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -64
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -78
[bluetooth]# sudo rfcomm bind rfcomm0 00:18:E4:34:E7:08
Invalid command in menu main: sudo

Use "help" for a list of available commands in a menu.
Use "menu <submenu>" if you want to enter any submenu.
Use "back" if you want to return to menu main.
[bluetooth]# rfcomm bind rfcomm0 00:18:E4:34:E7:08
Invalid command in menu main: rfcomm

Use "help" for a list of available commands in a menu.
Use "menu <submenu>" if you want to enter any submenu.
Use "back" if you want to return to menu main.
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -68
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -88
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -67
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -86
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -77
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -67
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -86
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -68
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -78
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -81
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -87
[NEW] Device 52:F5:D6:90:D6:3E 52-F5-D6-90-D6-3E
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -77
[CHG] Device 52:F5:D6:90:D6:3E RSSI: -90
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -87
[NEW] Device 6A:64:59:0B:F4:44 6A-64-59-0B-F4-44
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -67
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -89
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -68
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -97
[CHG] Device 00:18:E4:34:E7:08 Connected: yes
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -78
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -74
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -88
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -88
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -65
[CHG] Device 00:18:E4:34:E7:08 Connected: no
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -79
[CHG] Device 00:18:E4:34:E7:08 Connected: yes
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -68
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -78
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -88
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -77
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -86
[CHG] Device 00:18:E4:34:E7:08 Connected: no
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -68
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -78
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -68
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -88
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -76
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -79
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -89
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -78
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -88
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -89
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -75
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -87
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -75
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -76
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Key: 0x004c
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Value:
  10 05 29 18 f7 e4 39                             ..)...9
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -86
[CHG] Device 61:24:0C:EA:AA:FC ManufacturerData Key: 0x004c
[CHG] Device 61:24:0C:EA:AA:FC ManufacturerData Value:
  10 06 54 1e f5 1c 1c 8e                          ..T.....
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -84
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -91
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -81
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -75
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -85
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -76
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Key: 0x004c
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Value:
  10 05 69 1c f7 e4 39                             ..i...9
[NEW] Device 6F:E5:A7:D4:F4:6A 6F-E5-A7-D4-F4-6A
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -90
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Key: 0x004c
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Value:
  10 05 29 18 f7 e4 39                             ..)...9
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -84
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -73
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -83
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -73
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -83
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -71
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -80
[CHG] Device 6A:64:59:0B:F4:44 RSSI: -74
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Key: 0x004c
[CHG] Device 6A:64:59:0B:F4:44 ManufacturerData Value:
  10 05 69 1c f7 e4 39                             ..i...9
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -88
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -82
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -100
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -92
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -92
[CHG] Device 61:24:0C:EA:AA:FC RSSI: -80
[CHG] Device 00:18:E4:34:E7:08 RSSI: -45
[CHG] Device 00:18:E4:34:E7:08 RSSI: -55
[NEW] Device 59:D7:D5:E4:07:B6 59-D7-D5-E4-07-B6
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -76
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -85
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -72
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -82
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -74
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -85
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -71
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -85
[NEW] Device 7E:9C:79:46:2E:B7 7E-9C-79-46-2E-B7
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -74
[CHG] Device 7E:9C:79:46:2E:B7 RSSI: -93
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -82
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -84
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -75
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -85
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -73
[CHG] Device 59:D7:D5:E4:07:B6 ManufacturerData Key: 0x004c
[CHG] Device 59:D7:D5:E4:07:B6 ManufacturerData Value:
  10 06 59 1e 09 af bb 42                          ..Y....B
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -84
[CHG] Device 7E:9C:79:46:2E:B7 RSSI: -79
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -73
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -86
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -96
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -78
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -86
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -78
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -82
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -87
[CHG] Device 59:D7:D5:E4:07:B6 ManufacturerData Key: 0x004c
[CHG] Device 59:D7:D5:E4:07:B6 ManufacturerData Value:
  10 06 59 1e 09 af bb 46                          ..Y....F
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -74
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -84
[CHG] Device 7E:9C:79:46:2E:B7 RSSI: -93
[bluetooth]# pi@raspberrypi:~ $ sudo bluetoothctl
Invalid command in menu main: pi@raspberrypi:~

Use "help" for a list of available commands in a menu.
Use "menu <submenu>" if you want to enter any submenu.
Use "back" if you want to return to menu main.
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -74
[CHG] Device 59:D7:D5:E4:07:B6 ManufacturerData Key: 0x004c
[CHG] Device 59:D7:D5:E4:07:B6 ManufacturerData Value:
  10 06 59 1e 09 af bb 42                          ..Y....B
[CHG] Device 59:D7:D5:E4:07:B6 RSSI: -92
[CHG] Device 7E:9C:79:46:2E:B7 ManufacturerData Key: 0x004c
[CHG] Device 7E:9C:79:46:2E:B7 ManufacturerData Value:
  10 05 29 18 90 48 6c                             ..)..Hl
[NEW] Device 61:36:56:F7:6A:F6 61-36-56-F7-6A-F6
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -86
[NEW] Device 73:86:1C:95:67:81 73-86-1C-95-67-81
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -76
[CHG] Device 61:36:56:F7:6A:F6 ManufacturerData Key: 0x004c
[CHG] Device 61:36:56:F7:6A:F6 ManufacturerData Value:
  10 06 54 1e 96 66 16 aa                          ..T..f..
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -90
[CHG] Device 49:C9:0A:C8:2F:52 RSSI: -95
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -75
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -86
[CHG] Device 61:36:56:F7:6A:F6 ManufacturerData Key: 0x004c
[CHG] Device 61:36:56:F7:6A:F6 ManufacturerData Value:
  10 06 54 1e 96 66 16 a6                          ..T..f..
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -71
[CHG] Device 61:36:56:F7:6A:F6 ManufacturerData Key: 0x004c
[CHG] Device 61:36:56:F7:6A:F6 ManufacturerData Value:
  10 06 14 1a 96 66 16 a6                          .....f..
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -83
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -70
[CHG] Device 61:36:56:F7:6A:F6 RSSI: -85
[bluetooth]#
