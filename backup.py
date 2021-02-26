import os, sys, datetime

import functions, logger, tests

def win7Backup(WS:str):
    stickynotesPaths = functions.getWin7StickyDirs()
    if len(stickynotesPaths) == 0:
        logger.printThenLog("No StickyNotes found to backup!", 'backup')
    else:
        logger.printThenLog("Found {} users that potentially have sticky notes to backup! They'll be listed below...".format(len(stickynotesPaths)), 'backup')
        print("\n")
        for sPath in stickynotesPaths:
            user = functions.listFromPath(sPath)[2]
            sNoteSource = os.path.join(sPath, 'StickyNotes.snt')
            sNoteDestination = functions.getBackupPath(sNoteSource, WS)
            if os.path.exists(sNoteSource):
                if not os.path.exists(sNoteDestination):
                    os.system("mkdir {}".format(sNoteDestination))

                functions.copy(sNoteSource, sNoteDestination)
                logger.printThenLog("'{}' > backing up".format(user), 'backup')

            else:
                logger.printThenLog("!'{}' has a StickyNotes directory, but no StickyNotes.snt!".format(user), 'backup')

    print('\n')
    tests.backupCheck(WS)
    #functions.copyBackupLogs(WS)

ts = datetime.datetime.now().ctime()
logger.logB('Backup attempt started on {}'.format(ts))

print('\n')

started = False
args = sys.argv
for i in range(len(args)):
    if args[i] == '-w' and len(args) > i + 1:
        WORK_STATION = sys.argv[i + 1]
        logger.printThenLog("Attempting to backup sticky notes for workstation: '{}'".format(WORK_STATION), 'backup')
        win7Backup(WORK_STATION)
        started = True
        break

if not started:
    logger.printThenLog("Did not find a workstation passed! Run the command as: 'backup.exe -w <workstation id>'", 'backup')
