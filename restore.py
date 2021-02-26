import os, sys, datetime

import functions, logger, tests

def win10Restore(WS:str):
    #get backups
    backup_paths = []
    for p in functions.getBackupPaths(WS):
        if os.path.exists(os.path.join("C:\\Users", functions.listFromPath(p)[-1])):
            backup_paths.append(p) #we only want to restore users that exist on the new ws
    if len(backup_paths) == 0:
        logger.ptLogR("No backups found for any user within workstation {}".format(WS))
    else:
        #for each backup, copy then rename
        logger.ptLogR("Found {} users that potentially have sticky notes to backup! They'll be listed below...".format(len(backup_paths)))
        print('\n')
        for p in backup_paths:
            user = functions.listFromPath(p)[-1]
            restore_path = functions.getWin10StickyDir(user)
            backup_path = os.path.join(p, 'StickyNotes.snt')
            if os.path.exists(backup_path):
                logger.ptLogR("'{}' > restoring".format(user))
                if not os.path.exists(restore_path):
                    os.system('MKDIR {}'.format(restore_path))
                functions.copy(backup_path, restore_path)
                restored_file = os.path.join(restore_path, 'StickyNotes.snt')
                if os.path.exists(restored_file):
                    #rename
                    os.system("RENAME {} {}".format(restored_file, 'ThresholdNotes.snt'))
            else:
                logger.ptLogR("!Could not find backup for user {}! (expected to find in {})".format(user, backup_path))

    tests.restoreCheck(WS)
    #functions.copyBackupLogs(WS)


ts = datetime.datetime.now().ctime()
logger.logR('Restore attempt started on {}'.format(ts))

print('\n')

started = False
args = sys.argv
for i in range(len(args)):
    if args[i] == '-w' and len(args) > i + 1:
        WORK_STATION = sys.argv[i + 1]
        logger.printThenLog("Attempting to restore sticky notes for workstation: '{}'".format(WORK_STATION), 'backup')
        win10Restore(WORK_STATION)
        started = True
        break

if not started:
    logger.printThenLog("Did not find a workstation passed! Run the command as: 'restore.exe -w <workstation id>'", 'backup')
