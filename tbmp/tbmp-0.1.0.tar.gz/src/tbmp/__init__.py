"""tbmp
By Al Sweigart al@inventwithpython.com

A Python module for displaying bitmaps in the terminal as strings of block characters."""


import array, sys

PILLOW_INSTALLED = True
try:
    from PIL import Image, ImageDraw, ImageColor
except ImportError:
    PILLOW_INSTALLED = False

__version__ = '0.1.0'

TOP_BLOCK = chr(9600)
BOTTOM_BLOCK = chr(9604)
FULL_BLOCK = chr(9608)

class TBMP:
    def __init__(self, width=80, height=25, pixels=None, default=False):
        self._width = width
        self._height = height

        if default:
            # Start with the bitmap completely full.
            self.fill()
        else:
            # Start with the bitmap completely empty.
            self.clear()

        # TODO bitmap will be used to prepopulate


    def applyFunc(self, funcStr):
        if isinstance(funcStr, str):
            # A vague attempt at mitigating malicious input since func is passed to eval(). Don't rely on this for security.
            if ';' in funcStr or 'import' in funcStr or 'open' in funcStr:
                raise Exception('funcStr argument as a string must only have a lambda funciton')

            if not funcStr.strip().replace(' ', '').lower().startswith('lambdax,y:'):
                funcStr = 'lambda x, y:' + funcStr
            func = eval(funcStr)

        for x in range(self._width):
            for y in range(self._height):
                self[x, y] = func(x, y)



    def png(self, fg='white', bg='black', fgAlpha=255, bgAlpha=255):
        if not PILLOW_INSTALLED:
            raise Exception('The png() function requires the Pillow module to be installed.')

        fg = ImageColor.getcolor(fg, 'RGB')
        if fgAlpha < 255:
            # Set the transparency of the foreground color:
            fg = (fg[0], fg[1], fg[2], fgAlpha)

        bg = ImageColor.getcolor(bg, 'RGB')
        if bgAlpha < 255:
            # Set the transparency of the foreground color:
            bg = (bg[0], bg[1], bg[2], bgAlpha)

        if fgAlpha < 255 or bgAlpha < 255:
            colorMode = 'RGBA'
        else:
            colorMode = 'RGB'
        im = Image.new(colorMode, (self._width, self._height), bg)

        draw = ImageDraw.Draw(im)
        pixels = []
        for x in range(self._width):
            for y in range(self._height):
                if self[x, y]:
                    pixels.append((x, y))

                    # Make calls to draw.point() with 10k pixel chunks
                    # to keep memory usage from getting too high:
                    if len(pixels) > 10000:
                        draw.point(pixels, fill=fg)
                        pixels.clear()
        draw.point(pixels, fill=fg)
        return im



    def clear(self):
        # Make the bitmap completely empty.
        numBytesNeeded = (self._width * self._height) // 8
        if (self._width * self._height) % 8 > 0:
            numBytesNeeded += 1
        self._bitmap = array.array('B', b'\x00' * numBytesNeeded)


    def fill(self):
        # Make the bitmap completely full.
        numBytesNeeded = (self._width * self._height) // 8
        if (self._width * self._height) % 8 > 0:
            numBytesNeeded += 1
        self._bitmap = array.array('B', b'\xFF' * numBytesNeeded)

    #def toggle(self, xy=None): # TODO - name this flip or invert?
    #    pass

    @property
    def width(self):
        return self._width


    @property
    def height(self):
        return self._height


    def __getitem__(self, key):
        x, y = key
        arrayIndex = (y * self._width + x)
        byteIndex = arrayIndex // 8
        bitIndex = arrayIndex % 8

        return (self._bitmap[byteIndex] >> bitIndex) % 2


    def __setitem__(self, key, value): # TODO - note, value must be bool. Any other int besides 0 or 1 will cause bugs.
        x, y = key
        arrayIndex = (y * self._width + x)
        byteIndex = arrayIndex // 8
        bitIndex = arrayIndex % 8

        bitValue = (self._bitmap[byteIndex] >> bitIndex) % 2  # TODO - can I & 1 this instead of % 2?

        if value and not bitValue:
            # Set the False bit to True:
            self._bitmap[byteIndex] += (2 ** bitIndex)
        elif not value and bitValue:
            # Clear the True bit to False:
            self._bitmap[byteIndex] -= (2 ** bitIndex)


    def __delitem__(self, key):
        x, y = key
        arrayIndex = (y * self._width + x)
        byteIndex = arrayIndex // 8
        bitIndex = arrayIndex % 8

        bitValue = (self._bitmap[byteIndex] >> bitIndex) % 2

        if bitValue:
            # Clear the True bit to False:
            self._bitmap[byteIndex] -= (2 ** bitIndex)


    def __str__(self):
        result = []
        for y in range(0, self._height, 2):
            for x in range(self._width):
                if self[x, y]:
                    topHalf = True
                else:
                    topHalf = False

                if y + 1 == self._height or not self[x, y + 1]:
                    bottomHalf = False
                else:
                    bottomHalf = True

                if topHalf and bottomHalf:
                    result.append(FULL_BLOCK)
                elif topHalf and not bottomHalf:
                    result.append(TOP_BLOCK)
                elif not topHalf and bottomHalf:
                    result.append(BOTTOM_BLOCK)
                else:
                    result.append(' ')
            result.append('\n')
        return ''.join(result)



class InfTBMP(TBMP):
    # a limitless tbmp that lets you also have negative coordinates.
    pass