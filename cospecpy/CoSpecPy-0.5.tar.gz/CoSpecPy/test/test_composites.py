from CoSpecPy.composites import Composite
from CoSpecPy.download import DownloadHandler
from CoSpecPy.plotting import ComparisonPlot
import pkg_resources
import os
from astropy.io import fits

print("Testing Composite")
test_aria2_download = DownloadHandler("aria2", 5, 10, "test_tmp")
test_aria2_download.clear_up()

example_speclist = os.path.abspath("test_tmp/example_speclist.txt")

example_composite = Composite("example_composite")
example_composite.set_download_handler(test_aria2_download)
example_composite.set_wavelength_grid(w_min = 1000, w_max = 3000, steps = 3000)
example_composite.set_normalisation(norm_low = 2575, norm_high = 2625)
print("Composite Setup Finished")

example_table = fits.open("test_table.fits")
example_table = example_table[1].data


ra = example_table['RA_1']
dec = example_table['DEC_1']

ra_2 = ra[20:]
dec_2 = dec[20:]
new_composite = Composite("Comparison Composite")
new_composite.set_download_handler(test_aria2_download)
new_composite.set_wavelength_grid(w_min = 1000, w_max = 3000, steps = 3000)
new_composite.set_normalisation(norm_low = 2575, norm_high = 2625)
new_composite.composite_from_coords(ra_2, dec_2, chunks = 1)

print("RA and DEC loaded")

example_composite.composite_from_coords(ra, dec, chunks = 1)

plotter = ComparisonPlot(1200, 1800)
plotter.add_composite(example_composite)
plotter.add_composite(new_composite)
plotter.plot_all()
#example_composite.plot_composite(None)
