import string
ChannelMap = dict.fromkeys(string.ascii_uppercase)
for key in ChannelMap :
    ChannelMap[key] = ord(key)-64# A=1 B=2 etc

print (ChannelMap)

