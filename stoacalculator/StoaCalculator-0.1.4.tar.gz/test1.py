import stoacalculator
#Derivatives & Integrals
from sympy import *
import numpy as np
# We have to make a constant a symbol
x = Symbol('x')
# Now the usage of this module
stoacalculator.derivatives(sin(x)+exp(x)*log(x))
stoacalculator.integrals(sin(x)+exp(x)*log(x))
