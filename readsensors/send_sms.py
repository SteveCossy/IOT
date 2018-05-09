# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
# Read your Account Sid and Auth Token from twilio.com/console

dataFile = '/home/pi/twilio_data_test'

# File contains: SID Auth_Token TargetTemp TargetFreq Frequency SID startMsg txtBody from_nbr to_nbr
# txtBody eg: Current Temps - This: %1 That: %2
fileContent = open(dataFile,'r')
comment = fileContent.readline()
account_sid = fileContent.readline()		# Twilio ID and Token
auth_token = fileContent.readline()
temp_target_parts = fileContent.readline()	# Target for Alert messages : How often to send Alerts
temp_frequency_s = fileContent.readline()	# How often to sent regular updates
this_msg = fileContent.readline()		# Text for the first message
msg_body = fileContent.readline()		# Message to send, with %1 & %2 representing two values to insert
msg_from = fileContent.readline()		# From phone number, as required by Twilio
msg_to = fileContent.readline()			# To phone number, which must be authorised in Twilio
fileContent.close()

target_temp_s,target_freq_s = temp_target_parts.split(":")


client = Client(account_sid, auth_token)
message = client.messages.create(body=msg_body,from_=msg_from,to=msg_to)

print(message.sid)

