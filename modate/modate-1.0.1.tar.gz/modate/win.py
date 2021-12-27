import click
import win32file, win32con
import pywintypes
from glob import glob
from datetime_matcher import DatetimeMatcher
dtmatcher = DatetimeMatcher()

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
        raise(click.BadParameter("File(s) '%s' not found" % format(filepath)))
    return(filepaths)


def filedatetime(filename,date_format):
    try:
        search = r''+date_format
        date = dtmatcher.extract_datetime(search, filename)
    except:
        raise(click.BadParameter("Date not found, please check the date format introduced: %s" % date_format))
    return(date)


def main(filepath,date,date_format,created,modified,accessed):

    # Find files
    print('Searching for files with %s' % filepath)
    filepaths = getFilepaths(filepath)
    print('Files found:')
    print(*filepaths, sep = '\n')

    # Modify dates
    for file in filepaths:
        filename = file.split('/')[-1]
        if date_format is not None:
            date = filedatetime(filename,date_format)
        print('Using date: %s for file %s' % (date.strftime('%Y-%b-%d %H:%M:%S'),filename))
        setWinFileDateTimes(file,date,created,modified,accessed)