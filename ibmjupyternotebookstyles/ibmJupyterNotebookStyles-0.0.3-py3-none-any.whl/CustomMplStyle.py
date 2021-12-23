
from ibmJupyterNotebookStyles.StylingBase import StyleComponent
import matplotlib.pyplot as plt
import os


class CustomMplStyle(StyleComponent):
    mpl_style_name = "ibm.mplstyle"

    def apply(self) -> None:
        here = os.path.abspath(os.path.dirname(__file__))
        plt.style.use(os.path.join(here, self.mpl_style_name))
