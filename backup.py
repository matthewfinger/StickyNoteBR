import os, sys

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
                logger.printThenLog("'{}' > attempting to backup".format(user), 'backup')

            else:
                logger.printThenLog("!'{}' has a StickyNotes directory, but no StickyNotes.snt!".format(user), 'backup')

    tests.backupCheck(WS)


started = False
args = sys.argv
for i in range(len(args)):
    if args[i] == '-w' and len(args) > i + 1:
        WORK_STATION = sys.argv[i + 1]
        logger.printThenLog("Attempting to create backup for workstation: '{}'".format(WORK_STATION), 'backup')
        win7Backup(WORK_STATION)
        started = True
        break

if not started:
    logger.printThenLog("Did not find a workstation passed! Run the command as: 'backup -w <workstation id>'", 'backup')
