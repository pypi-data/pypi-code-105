from .download import DownloadHandler
from .composite_helpers import *

import scipy.interpolate as interp
import numpy as np
from astropy.io import fits

from subprocess import call
from glob import glob

import pkg_resources


class Composite:
    '''Composite Class to handle creation of composites

        Attributes:
            name (str): Name given to created Composite. Used in Plotting
    '''

    def __init__(self, name):

        self.name = name
        self.fluxes = []

    def reset_composite(self):
        '''Reset the flux list to an empty list'''
        self.fluxes = []

    def get_fluxes(self):
        ''' Return the current flux list

        Returns:
            (numpy array): An array containing each normalised spectra as a different
                                    element
        '''
        return np.array([item for sublist in self.fluxes for item in sublist])

    def get_composite(self, samples = 1):
        '''Return the averaged composite with bootstrapped uncertainties if chosen

            This will collect the normalised fluxes and take the median as the overall composite.
            If the number of samples is specified it will also calculate the uncertainty through
            bootstrapping and return this along with the median.

            Args:
                samples (int, optional): Number of bootstrap samples to take.

            Returns:
                (tuple): tuple containing:
                    median_flux (array): Array of the composite at each point on the wavelength grid.
                    bootstrap_std (array, optional): Bootstrapped uncertainty at each point on the wavelength grid.
        '''
        fluxes = np.array([item for sublist in self.fluxes for item in sublist])
        if samples == 1:
            median_flux = np.nanmedian(fluxes, axis = 0)
            return median_flux

        else:
            median_flux, bootstrap_std = boostrap_fluxes(fluxes, samples)
            return median_flux, bootstrap_std

    def set_download_handler(self, handler):
        ''' Set the download handler for in-built fetching of spectra

            Args:
                handler (DownloadHandler): Input download handler instance. Will control future SDSS downloads.
        '''
        if isinstance(handler, DownloadHandler):
            self.download_handler = handler
        else:
            raise Exception("Handler must be valid DownloadHandler")

    def set_wavelength_grid(self, w_min, w_max, steps):
        ''' Add the common wavelength grid

            Creates a numpy linspace which is used to interpolate SDSS spectra. Takes form np.linspace(w_min, w_max, steps).
            Wavelength is in Angstroms.

            Args:
                w_min (float): Minimum wave;ength for grid in Angstroms
                w_max (float): Maximum wavelength for grid in Ansgtroms
                steps (int): Number of points in the wavelength grid linspace
        '''
        self.w_min = w_min
        self.w_max = w_max
        self.wavelength_grid = np.linspace(w_min, w_max, steps)

    def set_normalisation(self, norm_low, norm_high):
        '''Add upper and lower normalisation values

            Normalisation is applied by dividing by the average value over a given
            wavelength range. This sets the upper and lower end of that range.

            Args:
                norm_low (float): Lower wavelength for normalisation in Angstrom
                norm_high (float): Upper wavelength for normalisation in Angstrom
        '''
        self.norm_low = norm_low
        self.norm_high = norm_high


    def composite_from_downloads(self, download_folder):
        '''Create composite from a directory of downloaded spectra

            Given a folder containing SDSS spectra downloads, create the normalised fluxes
            and store within the class

            Args:
                download_folder (string): Path to the folder where spectra are downloaded as .fits files.
        '''

        file_list = glob(download_folder+"/*spec**.fits")
        output_fluxes = [] #Initalise empty list for fluxes

        composite_run(file_list, self.wavelength_grid,
                        output_fluxes, self.norm_low, self.norm_high)
        self.fluxes.append(output_fluxes) #Add to the current flux list


    def save_composite(self, filename):
        '''Save current set of fluxes to .npy file

            Args:
                filename (str): Output filename for composite. Must be .npy extension.
        '''
        write_output(filename, self.fluxes)



    def composite_from_speclist(self, speclist, chunks = 1):
        '''Create a composite from speclist

            From a valid speclist.txt file cotaining valid SDSS URLs, download all spectra and create a composite.

            Args:
                speclist (str): Path to speclist file
                chunks (int, optional): Number of smallr chunks to split composite processing into. Useful if disc space is an issue.
        '''
        if chunks == 1:
            self.download_handler.clear_up()
            self.download_handler.download_spectra(speclist)
            self.composite_from_downloads(self.download_handler.download_folder)


        elif chunks > 1:
            glob_speclist = glob(os.path.dirname(speclist) +"/*[0-9]**.txt")
            call(['rm', '-r'] + glob_speclist)
            splitfile(speclist, chunks)
            glob_speclist = glob(os.path.dirname(speclist) +"/*[0-9]**.txt")
            print(glob_speclist)
            for file in glob_speclist:
                self.download_handler.clear_up()
                self.download_handler.download_spectra(file)
                self.composite_from_downloads(self.download_handler.download_folder)
                self.download_handler.clear_up()

        else:
            raise Exception("Chunks must be an integer defining the number of" +
                                " files to split the speclist into.")


    def composite_from_table(self, table, chunks = 1):
        '''Composite from an Astropy Table

            Create a composite from an Astropy table, produces speclist files as an intermediary

            Args:
                table (Astropy.Table): Valid astropy Table containing the sample. Must have columns PLATE, MJD and FIBERID.
                chunks (int, optional): Number of smaller chunks to split composite processing into. Useful if disc space is an issue.
        '''
        create_speclist(table, self.download_handler.download_folder) #Use helper function to create speclist
        print(self.download_handler.download_folder+"/speclist.txt")
        self.composite_from_speclist(self.download_handler.download_folder+"/speclist.txt", chunks)


    def composite_from_coords(self, ra, dec, catalogue = None, chunks = 1):
        '''Create composite from RA and DEC

            Download and create composite spectra from a list of ra and dec positions in degrees. Requires
            the SDSS DR14 or SDSS DR12 catalogue. If no path provided it will download one.

            Args:
                ra (list or array): Right Ascension of objects for composite in degrees
                dec (list or array): Declination of objects for composite in degrees
                catalogue (str, optional): Path to already existing DR14 or DR12 catalogue
                chunks (int, optional): Number of smaller chunks to split download into
        '''
        from astropy.coordinates import match_coordinates_sky, SkyCoord
        import astropy.units as u

        if catalogue == None:
            self.download_handler.get_DR14_quasars()
            catalogue_path = os.path.abspath(self.download_handler.download_folder)+"/DR14Q_v4_4.fits"

        else:
            catalogue_path = os.path.abspath(catalogue)

        print("Catalogue is located at %s"%catalogue_path)
        quasar_catalogue = fits.open(catalogue_path)[1].data

        catalogue_coords = SkyCoord(ra = quasar_catalogue['RA']*u.degree,
                                        dec = quasar_catalogue['DEC']*u.degree)

        target_coords = SkyCoord(ra = ra*u.degree, dec = dec*u.degree)

        best_match = target_coords.match_to_catalog_sky(catalogue_coords)

        print(best_match)

        best_match_SDSS = quasar_catalogue[best_match[0]]

        self.composite_from_table(best_match_SDSS, chunks)

        






    def plot_composite(self, output_figure = None):
        '''Simple plot of the current composite

            Args:
                output_figure (str, optional): Optional specification for a filename at which to save the composite plot. Will otherwise simply show the plot.
        '''

        import matplotlib.pyplot as plt

        flat_fluxes = np.array([item for sublist in self.fluxes for item in sublist]) #Flatten it all
        print(flat_fluxes)

        median_flux, std_flux = boostrap_fluxes(flat_fluxes, 500)
        plot_flux = median_flux*3e8/self.wavelength_grid
        difference = std_flux*3e8/self.wavelength_grid


        plt.figure(figsize = (12, 7))
        plt.plot(self.wavelength_grid, plot_flux, linewidth = 0.5)
        plt.fill_between(self.wavelength_grid, plot_flux-difference,
                            plot_flux+difference, alpha = 0.5)
        plt.xlabel(r"$\lambda$ [Å]", fontsize = 'xx-large')
        plt.ylabel(r"$F \nu$", fontsize = 'xx-large')
        plt.yscale('log')
        plt.xlim(self.w_min, self.w_max)
        plt.title("Composite: %s"%self.name)

        if output_figure == None:
            plt.show()
        elif len(output_figure)>0:
            plt.savefig(output_figure)
        else:
            plt.show()




    def example_from_downloads(self, download_folder):
        '''Full example run using the already downloaded list

            Run an example composite creation using some default values.

            Args:
                download_folder (str): Path to where the spectra are downloaded in .fits format.

        '''
        self.set_wavelength_grid(1000, 3000, 2500)
        self.set_normalisation(2575, 2625)
        self.composite_from_downloads(download_folder)
        self.plot_composite()
