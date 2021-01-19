# Testing write to file routines

import datetime, time, csv, os, struct

CrLf = '\r\n'
tempFile = '/tmp/writeOneLine.txt'
cs = '5'

port = open(tempFile, "w" )

port.write(cs+CrLf)

port.close
