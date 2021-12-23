"""fluffygoggles
By Al Sweigart al@inventwithpython.com

A Python app for taking a screenshot, reading the text with OCR, and copying the text to the clipboard. And it's free."""

"""
TODO for future versions:
pop up a notepad-like window with tkinter to show the text.
Have a quiet mode that disables this.
pop up with a window containing the screenshot, letting you outline the rectangular area to read.
"""


__version__ = '0.1.0'

import pyperclip, pyscreeze, os
import pytesseract as tess
from PIL import Image


def readScreen():
    print('Taking screenshot...')
    im = pyscreeze.screenshot('_deleteme-fluffygoggles.png')
    img = Image.open('_deleteme-fluffygoggles.png')
    print('Recognizing text in screenshot...')
    text = tess.image_to_string(img)

    text = text[:-1]  # Cut off the <0xC> character that pytesseract puts at the end.

    os.unlink('_deleteme-fluffygoggles.png')
    pyperclip.copy(text)
    print('Done.')

