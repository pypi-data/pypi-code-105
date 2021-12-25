from PIL import Image
from io import BytesIO
import win32clipboard


def MyPasteImg(filepath):
    image = Image.open(filepath)
    output = BytesIO()
    image.save(output, 'BMP')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, output.getvalue()[14:])
    win32clipboard.CloseClipboard()
    output.close()