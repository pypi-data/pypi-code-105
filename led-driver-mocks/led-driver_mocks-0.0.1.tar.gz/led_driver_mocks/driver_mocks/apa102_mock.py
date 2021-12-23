from functools import reduce
from math import ceil
from ..server.led_simulator import LedSimulator
from sys import modules

RGB_MAP = {'rgb': [3, 2, 1], 'rbg': [3, 1, 2], 'grb': [2, 3, 1],
           'gbr': [2, 1, 3], 'brg': [1, 3, 2], 'bgr': [1, 2, 3]}


class APAMock:
    host = '127.0.0.1'
    port = 40506
    MAX_BRIGHTNESS = 31  # Safeguard: Max. brightness that can be selected.
    LED_START = 0b11100000  # Three "1" bits, followed by 5 brightness bits
    BUS_SPEED_HZ = 8000000  # SPI bus speed; If the strip flickers, lower this value
    last_led_values_shown = None

    def __init__(self, num_led, global_brightness=MAX_BRIGHTNESS,
                 order='rgb', mosi=10, sclk=11, bus_speed_hz=BUS_SPEED_HZ,
                 ce=None):
        self.num_led = num_led
        self.order = order
        self.mosi = mosi
        self.sclk = sclk
        self.ce = ce
        self.server = LedSimulator(str(self.host), self.port)
        order = order.lower()
        self.rgb = RGB_MAP.get(order, RGB_MAP['rgb'])
        # Limit the brightness to the maximum if it's set higher
        if global_brightness > self.MAX_BRIGHTNESS:
            self.global_brightness = self.MAX_BRIGHTNESS
        else:
            self.global_brightness = global_brightness

        self.leds = [self.LED_START, 0, 0, 0] * self.num_led  # Pixel buffer

    def show(self):
        pixel_changed = False
        if self.last_led_values_shown is not None:
            for i in range(len(self.last_led_values_shown)):
                pixel_changed = self.last_led_values_shown[i] != self.leds[i]
                if pixel_changed:
                    break
        self.last_led_values_shown = self.leds.copy()
        if pixel_changed:
            leds = self.parse_leds(self.leds)
            msg = {
                'leds': leds,
                'mosi': self.mosi,
                'sclk': self.sclk,
            }
            self.server.send_led_data(msg)

    def clock_start_frame(self):
        pass

    def clock_end_frame(self):
        pass

    def clear_strip(self):
        """ Turns off the strip and shows the result right away."""

        for led in range(self.num_led):
            self.set_pixel(led, 0, 0, 0)
        self.show()

    def set_pixel(self, led_num, red, green, blue, bright_percent=100):
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer. Colors are passed individually.
        If brightness is not set the global brightness setting is used.
        """
        if led_num < 0:
            return  # Pixel is invisible, so ignore
        if led_num >= self.num_led:
            return  # again, invisible

        # Calculate pixel brightness as a percentage of the
        # defined global_brightness. Round up to nearest integer
        # as we expect some brightness unless set to 0
        brightness = ceil(bright_percent * self.global_brightness / 100.0)
        brightness = int(brightness)

        # LED startframe is three "1" bits, followed by 5 brightness bits
        ledstart = (brightness & 0b00011111) | self.LED_START

        start_index = 4 * led_num
        self.leds[start_index] = ledstart
        self.leds[start_index + self.rgb[0]] = red
        self.leds[start_index + self.rgb[1]] = green
        self.leds[start_index + self.rgb[2]] = blue

    def set_pixel_rgb(self, led_num, rgb_color, bright_percent=100):
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer.
        Colors are passed combined (3 bytes concatenated)
        If brightness is not set the global brightness setting is used.
        """
        self.set_pixel(led_num, (rgb_color & 0xFF0000) >> 16,
                       (rgb_color & 0x00FF00) >> 8, rgb_color & 0x0000FF,
                       bright_percent)

    def rotate(self, positions=1):
        """ Rotate the LEDs by the specified number of positions.

        Treating the internal LED array as a circular buffer, rotate it by
        the specified number of positions. The number could be negative,
        which means rotating in the opposite direction.
        """
        cutoff = 4 * (positions % self.num_led)
        self.leds = self.leds[cutoff:] + self.leds[:cutoff]

    def cleanup(self):
        """Release the SPI device; Call this method at the end"""
        print('Strip closed')

    @staticmethod
    def combine_color(red, green, blue):
        """Make one 3*8 byte color value."""

        return (red << 16) + (green << 8) + blue

    def wheel(self, wheel_pos):
        """Get a color from a color wheel; Green -> Red -> Blue -> Green"""

        if wheel_pos > 255:
            wheel_pos = 255  # Safeguard
        if wheel_pos < 85:  # Green -> Red
            return self.combine_color(wheel_pos * 3, 255 - wheel_pos * 3, 0)
        if wheel_pos < 170:  # Red -> Blue
            wheel_pos -= 85
            return self.combine_color(255 - wheel_pos * 3, 0, wheel_pos * 3)
        # Blue -> Green
        wheel_pos -= 170
        return self.combine_color(0, wheel_pos * 3, 255 - wheel_pos * 3)

    def dump_array(self):
        """For debug purposes: Dump the LED array onto the console."""

        print(self.leds)

    def _group_leds(self, leds, ledValue):
        if len(leds[len(leds) - 1]) == 4:
            leds.append([ledValue])
        else:
            leds[len(leds) - 1].append(ledValue)
        return leds

    def _parse_to_dict(self, ledList, led):
        ledList.append({
            'alpha': led[0],
            'blue': led[self.rgb[2]],
            'green': led[self.rgb[1]],
            'red': led[self.rgb[0]],
        })
        return ledList

    def parse_leds(self, leds):
        led_groups = reduce(self._group_leds, leds, [[]])
        return reduce(self._parse_to_dict, led_groups, [])


APA102 = APAMock


class _APA102:
    APA102 = APAMock


class _Driver:
    apa102 = _APA102


def setup_apa102_mock(server_address='127.0.0.1', port=40506):
    APAMock.host = server_address
    APAMock.port = port
    modules['apa102_pi'] = {'driver', _Driver}
    modules['apa102_pi.driver'] = _Driver
    modules['apa102_pi.driver.apa102'] = _APA102
