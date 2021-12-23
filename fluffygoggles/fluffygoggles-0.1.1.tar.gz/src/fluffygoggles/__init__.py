"""fluffygoggles
By Al Sweigart al@inventwithpython.com

A Python app for taking a screenshot, reading the text with OCR, and copying the text to the clipboard. And it's free."""

"""
TODO for future versions:
pop up with a window containing the screenshot, letting you outline the rectangular area to read.
compile this into a binary
"""


__version__ = '0.1.1'

import pyperclip, pyscreeze, os, sys, easygui, argparse
import pytesseract as tess
from PIL import Image




def readScreen(dontCopyToClipboard=False):
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument(dest='imageFilename', type=str, default=None, nargs='?', help="The filename of an image to read instead of taking a screenshot.")
    parser.add_argument('-q', '--quiet', dest='quietMode', action='store_const',
                    const=True, default=False,
                    help='quiet mode which suppresses output and the result text window')
    args = parser.parse_args()

    imageFilename = os.path.realpath(args.imageFilename)
    quietMode = args.quietMode
    screenshotMode = imageFilename is None

    if not quietMode:
        if imageFilename is None:
            print('Taking screenshot...')
        else:
            print('Reading image file ' + imageFilename + '...')

    if screenshotMode:
        im = pyscreeze.screenshot('_deleteme-fluffygoggles.png')
        img = Image.open('_deleteme-fluffygoggles.png')
    else:
        try:
            img = Image.open(imageFilename)
        except FileNotFoundError:
            sys.stderr.write('Could not find the file ' + imageFilename + '\n')
            sys.exit(1)

    if not quietMode:
        print('Recognizing text in screenshot...')

    text = tess.image_to_string(img)

    text = text[:-1]  # Cut off the <0xC> character that pytesseract puts at the end.

    if screenshotMode:
        os.unlink('_deleteme-fluffygoggles.png')

    if not dontCopyToClipboard:
        pyperclip.copy(text)

    if not args.quietMode:
        print('Done. Text is:')
        print(text)
        easygui.textbox('The following has been copied to the clipboard:', 'Fluffy Goggles', text)

    return text
