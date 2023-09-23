#!/usr/bin/env python
import cayenne.client, datetime, time, serial, logging

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "3bc69df0-6ead-11e8-8e48-275f329dc9d5"
MQTT_PASSWORD  = "0a1ecb3d7d05288aa5691633c0d5632933819243"
MQTT_CLIENT_ID = "257f97e0-ef04-11ed-8485-5b7d3ef089d0"

# Default location of serial port on pre 3 Pi models
#SERIAL_PORT =  "/dev/ttyAMA0"

# Default location of serial port on Pi models 3 and Zero
SERIAL_PORT = "/dev/ttyS0"
#SERIAL_PORT = "/dev/rfcomm0" 

#This sets up the serial port specified above. baud rate is the bits per second timeout seconds
#port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

#This sets up the serial port specified above. baud rate and WAITS for any cr/lf (new blob of data from picaxe)
port = serial.Serial(SERIAL_PORT, baudrate=2400)

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, loglevel=logging.INFO)
#client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, loglevel=logging.DEBUG)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

qos = 1
qos_good = 1
#qos_bad = 1
timestamp = 1

while True:
  client.loop()
  try:
    rcv = port.readline() #read buffer until cr/lf
    #print("Serial Readline Data = " + rcv)
    #rcv = rcv.rstrip("\r\n")
    synch,node,channel,data,cs = rcv.split(",")
    #print("rcv.split Data = : " + node + " " + channel + " " + data + " " + cs)
    #time.sleep(1)
    #Pacing delay to control rate of upload data

    checkSum = (int(node) + int(channel) + int(data))
    cs = int(cs)
    #print(checkSum,cs)

    if checkSum == cs:
      qos_good = qos_good + 1
      time.sleep(.1)
      #Wait a bit for Serial Ports
      port.write (str(cs) + "\r\n")
      #ASCII numeric CheckSum + CR,LF new line terminator
    #else :
      #qos_bad = qos_bad + 1
      #client.virtualWrite(26,qos_bad, "analog_sensor", "null")
      #print(qos_good,qos_bad)

    if (time.time() > timestamp):
      #qos = float(qos_good) / (qos_good + qos_bad)		#Calculate error rate ratio
      #qos = round(qos,2) * 100					#Convert qos ratio to Percent
      client.virtualWrite(25,qos_good,"analog_sensor", "null")
      #client.virtualWrite(25,qos_bad, "analog_sensor", "null")
      qos_good  = 1
      #qos_bad   = 1
      timestamp = time.time() + 300 				#Every xxx seconds 300 = 5 minutes

    if checkSum == int(cs) :
    #if cs = Check Sum is good then do the following

      if channel == '1':
        data = float(data)/1
        client.virtualWrite(1, data, "analog_sensor", "null")

      if channel == '2':
        data = float(data)/1
        client.virtualWrite(2, data, "analog_sensor", "null")

      if channel == '3':
        data = float(data)/1
        client.virtualWrite(3, data, "analog_sensor", "null")

      if channel == '4':
        data = float(data)/1
        client.virtualWrite(4, data, "analog_sensor", "null")

      if channel == '5':
        data = float(data)/1
        client.virtualWrite(5, data, "analog_sensor", "null")

      if channel == '6':
        data = float(data)/1
        client.virtualWrite(6, data, "analog_sensor", "null")

      if channel == '7':
        data = float(data)/1
        client.virtualWrite(7, data, "analog_sensor", "null")

      if channel == '8':
        data = float(data)/1
        client.virtualWrite(8, data, "analog_sensor", "null")

      if channel == '9':
        data = float(data)/1
        client.virtualWrite(9, data, "analog_sensor", "null")

      if channel == '10':
        data = float(data)/1
        client.virtualWrite(10, data, "analog_sensor", "null")

      if channel == '11':
        data = float(data)/1
        client.virtualWrite(11, data, "analog_sensor", "null")

      if channel == '12':
        data = float(data)/1
        client.virtualWrite(12, data, "analog_sensor", "null")

      if channel == '13':
        data = float(data)/1
        client.virtualWrite(13, data, "analog_sensor", "null")

      if channel == '14':
        data = float(data)/1
        client.virtualWrite(14, data, "analog_sensor", "null")

      if channel == '15':
        data = float(data)/1
        client.virtualWrite(15, data, "analog_sensor", "null")

      if channel == '16':
        data = float(data)/1
        client.virtualWrite(16, data, "analog_sensor", "null")

      if channel == '17':
        data = float(data)/1
        client.virtualWrite(17, data, "analog_sensor", "null")

      if channel == '18':
        data = float(data)/1
        client.virtualWrite(18, data, "analog_sensor", "null")

      if channel == '19':
        data = float(data)/1
        client.virtualWrite(19, data, "analog_sensor", "null")

      if channel == '20':
        data = float(data)/1
        client.virtualWrite(20, data, "analog_sensor", "null")

      if channel == '21':
        data = float(data)/1
        client.virtualWrite(21, data, "analog_sensor", "null")

      if channel == '22':
        data = float(data)/1
        client.virtualWrite(22, data, "analog_sensor", "null")

      if channel == '23':
        data = float(data)/1
        client.virtualWrite(23, data, "analog_sensor", "null")

      if channel == '24':
        data = float(data)/1
        client.virtualWrite(24, data, "analog_sensor", "null")

      if channel == '25':
        data = float(data)/1
        client.virtualWrite(25, data, "analog_sensor", "null")

      if channel == '26':
        data = float(data)/1
        client.virtualWrite(26, data, "analog_sensor", "null")

      if channel == '30':
        data = float(data)/1
        client.virtualWrite(30, data, "analog_sensor", "null")

      if channel == '31':
        data = float(data)/1
        client.virtualWrite(31, data, "analog_sensor", "null")

      if channel == '32':
        data = float(data)/1
        client.virtualWrite(32, data, "analog_sensor", "null")

      if channel == '33':
        data = float(data)/1
        client.virtualWrite(33, data, "analog_sensor", "null")

      if channel == '34':
        data = float(data)/1
        client.virtualWrite(34, data, "analog_sensor", "null")

      if channel == '35':
        data = float(data)/1
        client.virtualWrite(35, data, "analog_sensor", "null")

      if channel == '36':
        data = float(data)/1
        client.virtualWrite(36, data, "analog_sensor", "null")

      if channel == '37':
        data = float(data)/1
        client.virtualWrite(37, data, "analog_sensor", "null")

      if channel == '38':
        data = float(data)/1
        client.virtualWrite(38, data, "analog_sensor", "null")

      if channel == '39':
        data = float(data)/1
        client.virtualWrite(39, data, "analog_sensor", "null")

      if channel == '51':
        data = float(data)/10
        client.virtualWrite(51, data, "analog_sensor", "null")

      if channel == '52':
        data = float(data)/10
        client.virtualWrite(52, data, "analog_sensor", "null")

      if channel == '53':
        data = float(data)/1
        client.virtualWrite(53, data, "analog_sensor", "null")

      if channel == '54':
        data = float(data)/1
        client.virtualWrite(54, data, "analog_sensor", "null")

      if channel == '55':
        data = float(data)/1
        client.virtualWrite(55, data, "analog_sensor", "null")

      if channel == '56':
        data = float(data)/1
        client.virtualWrite(56, data, "analog_sensor", "null")

      if channel == '57':
        data = float(data)/1
        client.virtualWrite(57, data, "analog_sensor", "null")

      if channel == '58':
        data = float(data)/1
        client.virtualWrite(58, data, "analog_sensor", "null")

      if channel == '59':
        data = float(data)/1
        client.virtualWrite(59, data, "analog_sensor", "null")

      if channel == '101':
        data = float(data)/1
        client.virtualWrite(101, data, "analog_sensor", "null")

      if channel == '102':
        data = float(data)/1
        client.virtualWrite(102, data, "analog_sensor", "null")

      if channel == '103':
        data = float(data)/1
        client.virtualWrite(103, data, "analog_sensor", "null")

      if channel == '104':
        data = float(data)/1
        if data >= 555:
          data = 0.1
        client.virtualWrite(104, data, "analog_sensor", "null")

      if channel == '105':
        data = float(data)/1
        if data >= 555:
          data = 0.1
        client.virtualWrite(105, data, "analog_sensor", "null")

      if channel == '106':
        data = float(data)/1
        if data == 0:
          data = 0.1
        if data >= 555:
          data = 0.1
        client.virtualWrite(106, data, "analog_sensor", "null")

  except ValueError:
    #qos_bad = qos_bad + 10
    #error = error + 10
    #error = float(error)/1
    #client.virtualWrite(22,error)/1
    #if Data Packet corrupt or malformed then...
    #qos_bad = qos_bad + 5
    #client.virtualWrite(25, qos_bad, "analog_sensor", "null")
    print("Data Packet corrupt or malformed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(qos_bad))



