import numpy as np
import scipy
from subprocess import call
import pkg_resources
from glob import glob
import os


class DownloadHandler:
    '''Control acces to SDSS spectra

        This class is used to handle all downloads from SDSS servers and can be customised
        by connection type and number to increase efficiency.

        Attributes:
            download_method (str): Valid download method of either `wget` or `aria2`. Controls the download of SDSS spectra
            no_of_connections (int): For `aria2` connection this defines the number of simultaneous connections to SDSS servers
            batch_size (int): Controls batch size of download (size of each chunk)
            download_folder (str): Path to desired download folder for all future downloads.
    '''

    def __init__(self, download_method, no_of_connections,
                    batch_size, download_folder):

        if download_method != "aria2" and download_method != "wget":
            raise Exception("Valid Download Method is either 'wget' or 'aria2'")
        self.download_method = download_method
        self.no_of_connections = no_of_connections
        self.batch_size = batch_size
        self.download_folder = os.path.abspath(download_folder)

    def download_spectra(self, download_file):
        '''Download spectra from a file.

        Given spectra list containing correctly formatted URLs, download
        using preferred method given in class initiation

        Args:
            download_file (str): Path to the file containing the valid URLs
        '''
        if self.download_method == "aria2":
            call(['aria2c', '-c', '--check-certificate=false',
            '-j', str(self.no_of_connections), '-i', download_file],
            cwd = self.download_folder)

        if self.download_method == "wget":
            call(['wget', '--no-check-certificate', '-c',
            '-i', download_file],
            cwd = self.download_folder)

    def download_example(self):
        ''' Download the example short spectra list in the data directory '''
        DATA_PATH = pkg_resources.resource_filename(__name__, 'data/example_speclist.txt')
        print(DATA_PATH)
        self.download_spectra(DATA_PATH)
        print("Downloaded Succesfully")

    def clear_up(self):
        '''Clear files away from the specified download_folder'''
        files = glob(self.download_folder+'/*spec**.fits')
        call(['rm','-r'] + files)

    def get_DR12_quasars(self):
        '''Get the 512MB DR12 catalogue for future matching'''

        if self.download_method == "wget":
            call(['wget', '--no-check-certificate', '-c',
            'http://data.sdss3.org/sas/dr12/boss/qso/DR12Q/DR12Q.fits'],
            cwd = self.download_folder)

        if self.download_method == "aria2":
            call(['aria2c', '-c', '--check-certificate=false',
            'http://data.sdss3.org/sas/dr12/boss/qso/DR12Q/DR12Q.fits'],
            cwd = self.download_folder)

    def get_DR14_quasars(self):
        '''Get the 750MB DR14 catalogue for future matching'''

        if self.download_method == "wget":
            print("Downloading DR14")
            call(['wget', '--no-check-certificate', '-c',
            'https://data.sdss.org/sas/dr14/eboss/qso/DR14Q/DR14Q_v4_4.fits'],
            cwd = self.download_folder)

        if self.download_method == "aria2":
            print("Downloading DR14")
            call(['aria2c', '-c', '--check-certificate=false',
            'https://data.sdss.org/sas/dr14/eboss/qso/DR14Q/DR14Q_v4_4.fits'],
            cwd = self.download_folder)
