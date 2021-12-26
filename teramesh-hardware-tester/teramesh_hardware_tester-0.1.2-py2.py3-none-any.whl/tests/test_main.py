
import asyncio
import logging
import sys
import termios
import tty


logger = logging.getLogger(__name__)


test_calibration_temperature = None
test_calibration_humidity = None


def getch():
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()


async def setup(AT):
    global test_calibration_temperature
    global test_calibration_humidity
    try:
        from sht85 import single_shot
        test_calibration_temperature, test_calibration_humidity = single_shot()
    except Exception as e:
        logger.warning('SHT85 failed to read: %s', e)


async def test_comms(AT):
    await AT.TESTCOMMS.execute()
    await AT.TESTCOMMS.expect_ok_or_error()


async def test_shtc3(AT):
    global test_calibration_temperature
    global test_calibration_humidity
    await AT.TESTSHTC3.execute()
    result = await AT.TESTSHTC3.expect_reply()
    temperature, humidity = result.strip().split(',')
    logger.info('SHTC3 temperature %s', temperature)
    logger.info('SHTC3 humidity %s', humidity)
    # FIXME: TODO: RPi could be connected to a calibration source and compare these to some ground truth
    assert 10 < float(temperature) < 50, 'SHTC3 returned erroneous temperature'
    assert 0 < float(humidity) < 100, 'SHTC3 returned erroneous humidity'
    if test_calibration_temperature is not None:
        logger.info('SHTC3 temperature offset: %f', test_calibration_temperature - float(temperature))
    if test_calibration_humidity is not None:
        logger.info('SHTC3 humidity offset: %f', test_calibration_humidity - float(humidity))


async def test_buzzer(AT):
    await AT.TESTBUZZ.execute()
    await AT.TESTBUZZ.expect_ok_or_error()
    logger.critical('Did the buzzer buzz (y/n)?')
    assert getch().lower() == 'y', 'Buzzer did not buzz'


async def test_led(AT):
    await AT.TESTLED.execute()
    await AT.TESTLED.expect_ok_or_error()
    logger.critical('Did the LED screen do the thing (y/n)?')
    assert getch().lower() == 'y', 'LED did not do the thing'


async def test_pir(AT):
    logger.critical('Please prepare to WAVE AT PIR!')
    for x in range(3, 0, -1):
        logger.critical(f'{x}...')
        await asyncio.sleep(1)
    logger.critical('WAVE!')
    await AT.TESTPIR.execute()
    result = await AT.TESTPIR.expect_reply()
    assert int(result) == 1, 'PIR did not detect waving'


async def test_btn(AT):
    # TESTBTN handler waits for 5 seconds
    await AT.TESTBTN.execute()
    logger.critical('Please prepare to PRESS DEV KEY!')
    logger.critical('3...')
    await asyncio.sleep(1)
    logger.critical('2...')
    await asyncio.sleep(1)
    logger.critical('1...')
    await asyncio.sleep(1)
    logger.critical('PRESS!')
    await AT.TESTBTN.expect_ok_or_error(timeout=15)


async def test_relays(AT):

    import RPi.GPIO as GPIO

    RELAY_COMMON_GPIO = 5
    RELAY_GPIO_MAP = {
        1: 4,
        2: 17,
        3: 27,
        4: 22,
        6: 24,
    }

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_COMMON_GPIO, GPIO.OUT)
    GPIO.output(RELAY_COMMON_GPIO, GPIO.HIGH)
    for relay_pin in RELAY_GPIO_MAP.values():
        GPIO.setup(relay_pin, GPIO.IN)

    try:
        await AT.TESTRELAY0.execute()
        await AT.TESTRELAY0.expect_ok_or_error()
        await asyncio.sleep(0.1)
        for relay_no, relay_pin in RELAY_GPIO_MAP.items():
            assert not GPIO.input(relay_pin), f'Relay {relay_no} did not close'
        for relay_no, relay_pin in RELAY_GPIO_MAP.items():
            await getattr(AT, f'TESTRELAY{relay_no}').execute()
            await getattr(AT, f'TESTRELAY{relay_no}').expect_ok_or_error()
            await asyncio.sleep(0.1)
            assert GPIO.input(relay_pin), f'Relay {relay_no} did not open'
    finally:
        GPIO.cleanup()
