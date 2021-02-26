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
        if os.path.exists(snFilePath) and os.path.exists(bkFilePath):
            passes += 1
            logger.logB("User {}'s sticky notes are successfully backed up to {}".format(user, bkFilePath))
        else:
            logger.logB("!User {}'s sticky notes did not backup".format(user))

    logger.ptLogB("{} / {} users' sticky notes backed up successfully".format(passes, total))
    if total != passes:
        logger.ptLogB("!{} users' sticky notes failed to back up! See .\\StickyNoteLogs\\backup.log for details...".format(total - passes))
