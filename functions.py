import os
import logger

WIN7_STICKYNOTE_PATTERN = os.path.join(*['AppData', 'Roaming', 'Microsoft', 'StickyNotes'])
WIN10_STICKYNOTE_PATTERN = os.path.join(*['AppData', 'Local', 'Packages', 'Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe', 'LocalState', 'Legacy'])

BACKUP_PATTERN = None

USER_FOLDER_PATTERN = os.path.join(*['C:\\Users'])
BACKUP_PATH = os.path.join(os.getcwd(), "StickyNotesBackups") #bug here

def getBackupPath(source, WS:str):
    pList = listFromPath(source)

    user = pList[2]
    return os.path.join(BACKUP_PATH, WS, user)


#converts a pathlike object, TREATED AS A STRING, to it's list compontents
def listFromPath(path):
    default = []
    try:
        out = path.split(os.sep)
        return out
    except Exception:
        return default


def getWin7StickyDirs():
    out = []
    for user in os.listdir(USER_FOLDER_PATTERN):
        newpath = os.path.join(USER_FOLDER_PATTERN, user, WIN7_STICKYNOTE_PATTERN)
        if os.path.isdir(newpath):
            out.append(newpath)
    return out

def getWin10StickyDirs():
    out = []
    for user in os.listdir(USER_FOLDER_PATTERN):
        newpath = os.path.join(USER_FOLDER_PATTERN, user, WIN10_STICKYNOTE_PATTERN)
        if os.path.isdir(newpath):
            out.append(newpath)
    return out


def getWin10StickyDir(user):
    newpath = os.path.join(USER_FOLDER_PATTERN, user, WIN10_STICKYNOTE_PATTERN)
    if not os.path.exists(newpath):
        os.system("mkdir {}".format(newpath))
    return newpath

def getWin10StickyDirsFromUsers(users):
    out = []
    for user in users:
        out.append(getWin10StickyDir(user))
    return out


def copy(source, destination):
    syscall = "XCOPY {} {} /E /C /H /R /K /O /Y".format(source, destination)
    try:
        os.system(syscall)
    except Exception:
        logger.printThenLog("Something went wrong copying {} to {}".format(source, destination))
