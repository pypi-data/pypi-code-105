""" Beewi SmartLight used by Home Assistant """
import logging
from bluepy import btle
import tenacity

_LOGGER = logging.getLogger(__name__)

class BeewiSmartLight:
    """ This class will interact with a Beewi SmartLight bulb """

    def __init__(self, mac, iface: str = "hci0", address_type: str = "public"):
        """ Initialize the BeewiSmartLight """
        self._mac = mac
        self._iface = iface
        self._address_type = address_type
        self.peripheral = btle.Peripheral()
    
    def turnOn(self):
        """ Turn on the light """
        command = "1001"
        try:
            self.__writeCharacteristic(command)
        except Exception as e:
            _LOGGER.error(e)

    def turnOff(self):
        """ Turn off the light """
        try:
            command = "1000"
            self.__writeCharacteristic(command)
        except Exception as e:
            _LOGGER.error(e)
        
    def setWhite(self):
        """ Switch the light in white mode """
        try:
            command = "14808080"
            self.__writeCharacteristic(command)
        except Exception as e:
            _LOGGER.error(e)
        
    def setColor(self, r:int, g:int, b:int):
        """ Switch the light in color mode and set the RGB color """
        try:
            hexR = str(hex(r)[2:]).zfill(2)
            hexG = str(hex(g)[2:]).zfill(2)
            hexB = str(hex(b)[2:]).zfill(2)
            command = "13" + hexR + hexG + hexB
            self.__writeCharacteristic(command)
        except Exception as e:
            _LOGGER.error(e)

    def setBrightness(self, brightness:int):
        """ Set the brightness of the light """
        try:
            brightnessten = 0 if brightness == 0 else (round((brightness / 2.55 ) / 10) + 1)
            command = "120" + str(hex(2 if brightnessten < 2 else brightnessten)[2:])
            self.__writeCharacteristic(command)
        except Exception as e:
            _LOGGER.error(e)

    def setWhiteWarm(self, warm:int):
        """ Set the tone of the light cold/hot """
        try:
            warmten = 0 if warm == 0 else (round((warm / 2.55 ) / 10) + 1)
            command = "110" + str(hex(2 if warmten < 2 else warmten)[2:])
            self.__writeCharacteristic(command)
        except Exception as e:
            _LOGGER.error(e)

    def getSettings(self, verbose = 0):
        """ Get current state of the light """
        try:
            self.__readSettings()
            if verbose:
                print("       ON/OFF : {}".format(self.isOn))
                print("  WHITE/COLOR : {}".format(self.isWhite))
                print("   BRIGHTNESS : {}".format(self.brightness))
                print("  TEMPERATURE : {}".format(self.temperature))
                print("COLOR (R/G/B) : {} {} {}".format(self.red, self.green, self.blue))

            return self.settings
        except Exception as e:
            _LOGGER.error(e)
        
    def __readSettings(self):
        """ Read settings of the light """
        try:
            self.settings = self.__readCharacteristic(0x0024)
            self.isOn = self.settings[0]
            
            if(0x2 <= (self.settings[1] & 0x0F) <= 0xB):
                self.isWhite = 1
                self.temperature = (self.settings[1] & 0x0F) - 2
            elif(0x0 <= (self.settings[1] & 0x0F) < 0x2):
                self.isWhite = 0
                self.temperature = "N/A"
            brightness = ((self.settings[1] & 0xF0) >> 4) - 2
            self.brightness = int(0 if brightness == 0 else (((brightness + 1) * 2.55) * 10))
            self.red = self.settings[2]
            self.green = self.settings[3]
            self.blue = self.settings[4]

            return self.settings
        except:
            raise
    
    @tenacity.retry(stop=(tenacity.stop_after_delay(10) | tenacity.stop_after_attempt(5)))
    def __writeCharacteristic(self,command):
        """ Send command to the light """
        try:
            self.peripheral.connect(self._mac)
            self.peripheral.writeCharacteristic(0x0021,bytes.fromhex("55" + command + "0d0a"))
            self.peripheral.disconnect()
        except:
            raise

    @tenacity.retry(stop=(tenacity.stop_after_delay(10) | tenacity.stop_after_attempt(5)))
    def __readCharacteristic(self,characteristic):
        """ Read BTLE characteristic """
        try:
            self.peripheral.connect(self._mac)
            resp = self.peripheral.readCharacteristic(characteristic)
            self.peripheral.disconnect()
            return resp
        except:
            raise