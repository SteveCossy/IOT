# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
# Read your Account Sid and Auth Token from twilio.com/console

dataFile = '/home/pi/twilio_data'

fileContent = open(dataFile,'r')
comment = fileContent.readline()
account_sid = fileContent.readline()
auth_token = fileContent.readline()
msg_body = fileContent.readline()
msg_from = fileContent.readline()
msg_to = fileContent.readline()
fileContent.close()

client = Client(account_sid, auth_token) 
message = client.messages.create(body=msg_body,from_=msg_from,to=msg_to)

print(message.sid)

