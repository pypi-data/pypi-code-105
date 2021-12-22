import pytest
from CoSpecPy.download import DownloadHandler

# print("TESTING WGET!")
# test_wget_download = DownloadHandler("wget", 1, 10, "test_tmp")
# test_wget_download.clear_up()
# test_wget_download.download_example()
# test_wget_download.clear_up()
# print("CLEARED UP WGET")
#
# print("TESTING ARIA2!")
# test_aria2_download = DownloadHandler("aria2", 5, 10, "test_tmp")
# test_aria2_download.clear_up()
# test_aria2_download.download_example()
# test_aria2_download.clear_up()
# print("CLEARED UP ARIA2")


from CoSpecPy import DownloadHandler, Composite # Import the Handler

output_dir = "test_tmp"

ra = [] # Input you ra values here
dec = [] # Input you dec values here

example_handler = DownloadHandler(download_method = "wget", #Download method (aria2 or wget)
no_of_connections = 1, batch_size="10", #Connections only apply to aria2, batches not implemented
 download_folder=output_dir) # output folder

#Example download with wget
example_handler.download_example()

#This will download the 50 example spectra in CoSpecPy/data/example_speclist.txt to your chosen output

example_composite = Composite(name = "example_composite") #Creation of Composite Class
example_composite.set_wavelength_grid(w_min = 1000, w_max = 3000, steps = 2500) #Add the desired wavelength grid in Angstrom
example_composite.set_normalisation(norm_low = 2575, norm_high = 2625) #Add desired normalisation range in Angstrom
example_composite.composite_from_downloads(output_dir) # Will create the composite
example_composite.plot_composite() # Plots the composite stored in the composite class with bootstrapped uncertainties
