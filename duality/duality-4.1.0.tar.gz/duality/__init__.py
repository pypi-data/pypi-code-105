'''

duality - Decorator functions for the vandal library.
=====================================================================

This is a connection to the __init__ file of the duality package.

AVAILABLE FEATURES IN THE PACKAGE:

	record (OBJECT/DECORATOR)
	-------------------

	duality.record is an object decorator class that stores menu options over functions and class methods for listing.
		print(help(duality.record)) in order to see available features.

	track (OBJECT/DECORATOR)
	------------

	duality.track is an object decorator class that tracks function behaviuor and stores it into a JSON file.
		print(help(duality.track)) in order to see available features.

'''

# imports relevant contents.
from duality.decorators.particles import (
    record,
    track,
)

# all relevant contents.
__all__ = [
    record,
    track,
]
