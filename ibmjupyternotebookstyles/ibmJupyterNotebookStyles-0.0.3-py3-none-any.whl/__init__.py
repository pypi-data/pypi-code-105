from ibmJupyterNotebookStyles.CustomColorMaps import CustomColorMaps
from ibmJupyterNotebookStyles.CustomCssStyling import CustomCssStyling
from ibmJupyterNotebookStyles.CustomMplStyle import CustomMplStyle
from ibmJupyterNotebookStyles.StylingBase import ConcreteVisitor


def apply_ibm_styles():
    customCssStyling = CustomCssStyling()
    components = [CustomColorMaps(), CustomMplStyle(), customCssStyling]
    visitor = ConcreteVisitor()

    for component in components:
        component.accept(visitor)
    
    '''
    Must return and IPython.core.display.HTML object so that Jupyter notebook can load css styles. 
    '''
    return customCssStyling.html
