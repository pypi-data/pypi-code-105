import click
import platform
import os
from glob import glob
from datetime import datetime
import pywintypes
import time

@click.command()
@click.option('-f', '--filepath', prompt=False, help='Filepath of the file(s) to modify. Accepts wildcard arguments.')
@click.option('-d', '--date', prompt=False, help='Date to be modified')
#@click.option('-df', '--date_in_filename', prompt=False)
@click.option('-c', '--created', is_flag=True, help='Change the "created" datetime')
@click.option('-m', '--modified', is_flag=True, help='Change the "modified" datetime')
@click.option('-a', '--accessed', is_flag=True, help='Change the "last opened" datetime')

def main(filepath,date,created,modified,accessed):
    # Returns list of filenames, handles wildcards
    filepaths = getFilepaths(filepath)

    # Convert date to datetime
    date = convertDate(date)
    if platform.system() == 'Windows':
        for file in filepaths:
            setWinFileDateTimes(file,date,created,modified,accessed)
    else:
        '''TBD'''

def getFilepaths(filepath):
    # Get all filepaths in case of wildcard
    filepaths = []
    filepaths = list(glob(filepath))
    if len(filepaths) == 0 and '*' not in filepath:
        raise(click.BadParameter("File '%s' not found" % format(filepath)))
    return(filepaths)

def convertDate(date):
    try:
        date = datetime.strptime(date, '%Y%m%d_%H%M%S')
    except:
        raise(click.BadParameter("Date '%s' has bad format" % date))
    return(date)

def setWinFileDateTimes(filePath,date,created,modified,accessed):
    import win32file, win32con

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

if __name__ == '__main__':
    main()