# Email using Gmail, reading configuration from dataFile

dataFile = '/home/pi/EmailConfig'

def send_mail(gmailUser, gmailPassword, fromAddress, recipient, message, subject ):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()

fileContent = open(dataFile,'r')	# Open the config file for reading
comment = fileContent.readline()	# First line is ignored
gmailUser = fileContent.readline()	# Gmail User Name to use
gmailPassword = fileContent.readline()	# Gmail password
fromAddress = fileContent.readline()	# From Address
recipient = fileContent.readline()	# Recipient to send message to
subject = fileContent.readline()	# Subject Text
message = fileContent.readline()	# Message to send

fileContent.close()

send_mail(gmailUser, gmailPassword, fromAddress, recipient, message, subject )

