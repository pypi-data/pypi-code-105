import os
from glob import glob
from subprocess import call
import click
from datetime import datetime


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
    print(filepath)
    filepaths = []
    filepaths = list(glob(filepath))
    if len(filepaths) == 0 and '*' not in filepath:
        raise(click.BadParameter("File '%s' not found" % format(filepath)))
    return(filepaths)


def main(filepath,date,created,modified,accessed):
    filepaths = getFilepaths(filepath)

    for file in filepaths:
        setMacFileDateTimes(file,date,created,modified,accessed)