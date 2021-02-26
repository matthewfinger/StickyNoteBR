import os

import logger, functions
WIN7SPATHS = functions.getWin7StickyDirs()
WIN10SPATHS = functions.getWin10StickyDirs()

def backupCheck(WS):
    backup_path = os.path.join(functions.BACKUP_PATH, WS)
    if not os.path.exists(backup_path):
        logger.ptLogB("No backups have been created for workstation: '{}'".format(WS))
    passes = 0
    total = 0
    for p in WIN7SPATHS:
        total += 1
        user = functions.listFromPath(p)[2]
        snFilePath = os.path.join(p, 'StickyNotes.snt')
        bkFilePath = os.path.join(backup_path, user, "StickyNotes.snt")
        if os.path.exists(snFilePath) and os.path.exists(bkFilePath): #Backup exists as expected
            passes += 1
            logger.logB("User {}'s sticky notes are successfully backed up to {}".format(user, bkFilePath))
        elif os.path.exists(p): #Backup definitely does NOT exist
            logger.logB("!User {} has a Roaming\\Microsoft\\StickyNotes directory, but no backup was created! Try Checking up on this!".format(user))
        else: #Something might possibly be hinky here
            logger.logB("!User {}'s sticky notes did not backup".format(user))


    logger.ptLogB("{} / {} users' sticky notes backed up successfully".format(passes, total))
    if total != passes:
        logger.ptLogB("!{} users' sticky notes might have failed to back up! See .\\StickyNoteLogs\\backup.log for details...".format(total - passes))


def restoreCheck(WS):
    backup_path = os.path.join(functions.BACKUP_PATH, WS)
    if not os.path.exists(backup_path):
        logger.ptLogR("No backups have been created for workstation: '{}'".format(WS))

    passes = 0
    total = 0
    for p in WIN10SPATHS:
        total += 1
        user = functions.listFromPath(p)[2]
        rsFilePath = os.path.join(p, "ThresholdNotes.snt")
        bkFilePath = os.path.join(backup_path, user, "StickyNotes.snt")
        if os.path.exists(bkFilePath) and os.path.exists(rsFilePath):
            bkContent, rsContent = functions.contents(bkFilePath), functions.contents(rsFilePath)
            if bkContent == rsContent:
                passes += 1
                logger.logR("User {}'s sticky notes have restored successfully!'".format(user))
                continue
        elif os.path.exists(os.path.join(backup_path, user)): #backup exists for the user
            logger.logR("!User {}'s sticky notes are backed up but did not restore'".format(user))
        else: #Something might possibly be hinky here
            logger.logR("!User {} has a legacy sticky notes directory, however something may be off".format(user))

    logger.ptLogR("{} / {} users' sticky notes restored successfully!".format(passes, total))
    if total != passes:
        logger.ptLogR("{} users' sticky notes might have failed to restore. See .\\StickyNoteLogs\\restore.log for more details...".format(total - passes))
