import click
import os
from glob import glob
from datetime import datetime
from datetime_matcher import DatetimeMatcher
dtmatcher = DatetimeMatcher()


def setMacFileDateTimes(filePath,date,created,modified,accessed):
    if created:
        os.system('SetFile -d "{}" {}'.format(date.strftime('%m/%d/%Y %H:%M:%S'), filePath))
    if modified:
        #os.system('SetFile -m "{}" {}'.format(date.strftime('%m/%d/%Y %H:%M:%S'), filePath))
        # atime must be a datetime
        stat = os.stat(filePath)
        # times must have two floats (unix timestamps): (atime, mtime)
        os.utime(filePath, times=(stat.st_atime, date.timestamp()))
    if accessed:
        # atime must be a datetime
        stat = os.stat(filePath)
        # times must have two floats (unix timestamps): (atime, mtime)
        os.utime(filePath, times=(date.timestamp(), stat.st_mtime))


def getFilepaths(filepath):
    # Get all filepaths in case of wildcard
    filepaths = []
    filepaths = list(glob(filepath))
    if len(filepaths) == 0 and '*' not in filepath:
        raise(click.BadParameter("File '%s' not found" % format(filepath)))
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
        setMacFileDateTimes(file,date,created,modified,accessed)