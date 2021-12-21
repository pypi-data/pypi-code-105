# ~*~ coding: utf-8 ~*~
#-
# Copyright © 2021
#       Dominik George <nik@naturalnet.de>
#-
# Provided that these terms and disclaimer and all copyright notices
# are retained or reproduced in an accompanying document, permission
# is granted to deal in this work without restriction, including un‐
# limited rights to use, publicly perform, distribute, sell, modify,
# merge, give away, or sublicence.
#
# This work is provided “AS IS” and WITHOUT WARRANTY of any kind, to
# the utmost extent permitted by applicable law, neither express nor
# implied; without malicious intent or gross negligence. In no event
# may a licensor, author or contributor be held liable for indirect,
# direct, other damage, loss, or other issues arising in any way out
# of dealing in the work, even if advised of the possibility of such
# damage or existence of a defect, except proven that it results out
# of said person’s immediate fault when using the work as intended.

""" Utility code to play MML on hardware using ESP boards
with MicroPython
"""

from machine import Pin, PWM
import time

def play(playlist, pin, duty=512):
    """ Play a playlist on a buzzer on a GPIO pin.

     playlist - the music to play
     pin - the number of the pin (which must support PWM)
     duty - the duty cycle to use (default 512 = 50%)
    """
    beeper = PWM(Pin(pin))

    for freq, length in playlist:
        # Scale down frequency because PWM only supports up to 1 kHz
        while freq > 1000:
            freq /= 2

        if freq == 0:
            # Frequency 0 breaks PWM; turn down volume instead
            beeper.duty(0)
        else:
            beeper.duty(duty)
            beeper.freq(int(freq))
        time.sleep(length)
