HOME_DIR =      os.environ['HOME']
import os
HOME_DIR =      os.environ['HOME']
from persistqueue import Queue
QUEUE_FILE =    'CayenneQ'
QueuePathFile = os.path.join(CSVPath, QUEUE_FILE)
CSVPath =       HOME_DIR
QueuePathFile = os.path.join(CSVPath, QUEUE_FILE)
CayQueue =      Queue("QueuePathFile")
CayQueue.get()
CayQueue.empty()
