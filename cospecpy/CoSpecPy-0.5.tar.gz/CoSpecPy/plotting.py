import matplotlib.pyplot as plt
from .composites import Composite
from .composite_helpers import *


class ComparisonPlot:
    '''Class for Multiple Composites

        This class handles the plotting of one or more composites on a single
        plot

        Attributes:
            composite_list (list[Composite]): Contains all the currently added composites
            w_low (float): Lowest plotting wavelength in Angstrom. Default = 0
            w_high (float): Highest plotting wavelength in Angstrom. Default = 3000
    '''

    def __init__(self, w_low = 0, w_high = 3000):
        self.composite_list = []
        self.w_low = w_low
        self.w_high = w_high

    def set_plotting_wavelength(self, w_low, w_high):
        ''' Set plotting wavelength range

            Args:
                w_low (float): Lowest plotting wavelength in Angstrom
                w_high (float): Highest plotting wavelength in Angstrom
        '''
        self.w_low = w_low
        self.w_high = w_high

    def add_composite(self, composite):
        '''Add a composite to the current composite list

            Args:
                composite (Composite): A valid composite class.
        '''
        self.composite_list.append(composite)



    def plot_all(self, figsize = (12, 7), ylim = None, fig_output = None):
        '''Plot all Composites

            Plot all of the composites currently within the class composite_list

            Args:
                figsize (tuple(float, float), optional): Figsize to path to maptlotlib. Default = (12,7)
                ylim (tuple(float, float), optional): ylim option for matplotlib. Default leaves it to matlotlib automatically
                fig_output (str, optional): Output filename. If not given then the figure is shown via GUI
        '''

        plt.figure(figsize = figsize)

        for composite in self.composite_list:
            flat_fluxes = np.array([item for sublist in composite.fluxes for item in sublist])
            median_flux, bootstrap_std = boostrap_fluxes(flat_fluxes, samples = 500)

            plot_flux = median_flux*3e8/composite.wavelength_grid
            difference = bootstrap_std*3e8/composite.wavelength_grid

            plt.plot(composite.wavelength_grid, plot_flux, linewidth = 0.5, label = composite.name)
            plt.fill_between(composite.wavelength_grid, plot_flux-difference, plot_flux+difference,
                                    alpha = 0.5)

        plt.xlim(self.w_low, self.w_high)

        if ylim != None:
            plt.ylim(ylim)

        plt.xlabel(r"$\lambda$ [Å]", fontsize = 'xx-large')
        plt.ylabel(r"$F \nu$", fontsize = 'xx-large')
        plt.yscale('log')

        if fig_output != None:
            plt.savefig(fig_output)
        else:
            plt.show()
