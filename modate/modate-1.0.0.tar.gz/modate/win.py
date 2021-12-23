import win32file, win32con
import pywintypes
import click
import glob

def setWinFileDateTimes(filePath,date,created,modified,accessed):
    # Convert datetimes to pywintypes
    ctime = pywintypes.Time(date) if created else None
    mtime = pywintypes.Time(date) if modified else None
    atime = pywintypes.Time(date) if accessed else None

    # change time stamps
    winfile = win32file.CreateFile(
        filePath, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)
    win32file.SetFileTime(winfile,ctime,atime,mtime)
    winfile.close()


def getFilepaths(filepath):
    # Get all filepaths in case of wildcard
    filepaths = []
    filepaths = list(glob(filepath))
    if len(filepaths) == 0 and '*' not in filepath:
        raise(click.BadParameter("File '%s' not found" % format(filepath)))
    return(filepaths)


def main(filepath,date,created,modified,accessed):
    filepaths = getFilepaths(filepath)

    for file in filepaths:
        setWinFileDateTimes(file,date,created,modified,accessed)