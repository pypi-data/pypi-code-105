import stoacalculator
import numpy as np
# We recommend to always use 100 linearly spaced numbers
x = np.linspace(-5, 5, 100)
# For trigonometry we recommend to use this configuration
x = np.linspace(-np.pi, np.pi, 100)
# Example of formulas
trigonometricformula = np.sin(x)
exponentialformula = np.exp(x)
# Usage of formulas
stoacalculator.biplot(x, trigonometricformula, exponentialformula)
