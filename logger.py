import os
from datetime import datetime

LOGPATH = os.path.join(os.getcwd(), 'StickyNoteLogs')
BACKUPLOG = os.path.join(LOGPATH, 'backup.log')
RESTORELOG = os.path.join(LOGPATH, 'restore.log')

def showLogInfo():
    print("Logs are stored in .\\StickyNoteLogs.\nPractically all necessary information regarding the backup/restore process will be in backup.log and restore.log respectively")

#returns string w/ current time
def timeStamp():
    return datetime.now().ctime()

def initializeLogs():
    ts = timeStamp()
    initTsLog = makeLog("Log initialized on %s" % ts)
    if not os.path.exists(LOGPATH):
        os.mkdir(LOGPATH)
        backupFile = open(BACKUPLOG, "a")
        backupFile.write(initTsLog)
        backupFile.close()

        restoreFile = open(RESTORELOG, "a")
        restoreFile.write(initTsLog)
        restoreFile.close()


def makeLog(message):
    return "LOG: {} \n".format(message)

def log(message, whichlog):
    message = makeLog(message)
    logFile = open(RESTORELOG, 'a')
    if whichlog.lower() == "backup":
        logFile.close()
        logFile = open(BACKUPLOG, "a")

    logFile.write(message)
    logFile.close()

#wrapper for log, prints first
def printThenLog(message, whichlog):
    print(message)
    log(message, whichlog)


def ptLogB(message):
    printThenLog(message, 'backup')

def ptLogR(message):
    printThenLog(mesage, 'restore')

def logB(message):
    log(message, 'backup')
    
def logR(message):
    log(message, 'restore')

initializeLogs()
