"""Top-level package for Flat styled Jupyter Notebooks."""

__author__ = """Rutger Berns"""
__email__ = 'rutgerb0000@gmail.com'
__version__ = '0.1.0'

print("Hello")

from IPython.core.display import HTML, display


def set_style():
    display(HTML("""
    <style>
    #notebook {
        background-color: #E5E5E5;
    }
    #notebook-container {
        box-shadow: none;
    }
    body {
        background-color: #E5E5E5;
    }
    </style>
    """))