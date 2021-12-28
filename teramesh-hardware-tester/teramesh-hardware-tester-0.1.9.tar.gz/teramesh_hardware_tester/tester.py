#!/bin/env python3

import asyncio
import click
import csv
import curses
import glob
import importlib
import logging
import os
import pathlib
import re
import subprocess
import sys
import tempfile

# idrc_esp_tools modules
from .idrc_esp_tools import analyze_nvs, serial_asyncio, at


logger = logging.getLogger('tester')
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(os.environ['HOME'], '.hwtester')

NVS_TESTING_KEY = 'fwtest'
NVS_TARGET_NAMESPACE = 'ESP-MDF'
exit_code = 0


class CursesHandler(logging.Handler):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def emit(self, record):
        try:
            msg = self.format(record)
            fs = "\n%s"
            if record.levelname.lower() == 'critical':
                self.screen.addstr(fs % msg, curses.A_STANDOUT)
            else:
                self.screen.addstr(fs % msg)
            self.screen.refresh()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class SerialTestRunner:

    def __init__(self, usb_port, baudrate):
        self.usb_port = usb_port
        self.baudrate = baudrate

    def set_nvs_testing_flag(self):

        partition_table_out = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR)
        partition_table_out.close()

        # dump partition table from a running node
        p = subprocess.run([
            'python3', '-m', 'esptool',
            '--after',
            'no_reset',
            '-p',
            self.usb_port,
            'read_flash',
            '0x8000',
            '0x1000',
            partition_table_out.name,
        ], capture_output=True, text=True)
        if p.stderr:
            logger.warning(p.stderr)
        p.check_returncode()
        logger.info('Dumped partition table')

        # read partition table to determine offset / size
        p = subprocess.run([
            'python3',
            os.path.join(BASE_DIR, 'idrc_esp_tools/gen_esp32part.py'),
            '-q',
            partition_table_out.name,
        ], capture_output=True, text=True)
        if p.stderr:
            logger.warning(p.stderr)
        p.check_returncode()
        for line in p.stdout.split('\n'):
            if ',data,nvs,' in line:
                _name, _type, _subtype, _offset, _size, _flags = line.strip().split(',')
                nvs_partition_offset = int(_offset)
                nvs_partition_size = int(_size)
                logger.info('Detected NVS partition sized %d', nvs_partition_size)

        nvs_partition_in = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR, suffix='.bin')
        nvs_partition_out = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR, suffix='.bin')
        nvs_partition_in.close()

        # dump NVS from a running node
        p = subprocess.run([
            'python3', '-m', 'esptool',
            '--after',
            'no_reset',
            '-p',
            self.usb_port,
            'read_flash',
            str(nvs_partition_offset),
            str(nvs_partition_size),
            nvs_partition_in.name,
        ], capture_output=True, text=True)
        if p.stderr:
            logger.warning(p.stderr)
        p.check_returncode()
        logger.info('Dumped NVS partition')

        nvs_csv_in = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR)
        nvs_csv_out = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR)

        # get CSV of NVS values
        with open(nvs_partition_in.name, 'rb') as f:
            nvs_data = f.read()
            analyze_nvs.verify_nvs_size(nvs_data)
            analyze_nvs.parse_nvs_binary(nvs_data)
            for line in analyze_nvs.get_nvs_data(only_namespace=NVS_TARGET_NAMESPACE):
                nvs_csv_in.write(line.encode() + b'\n')
            nvs_csv_in.close()
        if p.stderr:
            logger.warning(p.stderr)
        p.check_returncode()
        logger.info('Converted NVS to CSV')

        # change vals in CSV
        testing_marker_found = False
        with open(nvs_csv_in.name) as csv_in:
            with open(nvs_csv_out.name, 'wt') as csv_out:
                reader = csv.DictReader(csv_in)
                writer = csv.DictWriter(csv_out, reader.fieldnames)
                writer.writeheader()
                for row in reader:
                    if row['key'] == NVS_TESTING_KEY:
                        testing_marker_found = True
                        if str(row['value']) in ['1', '01']:
                            logger.warning('Testing marker was set!')
                        row['encoding'] = 'u8'
                        row['value'] = '1'
                    writer.writerow(row)
                if not testing_marker_found:
                    writer.writerow({
                        'key': NVS_TESTING_KEY,
                        'type': 'data',
                        'encoding': 'u8',
                        'value': '1',
                    })
        logger.info('Set testing marker')

        # generate partition
        p = subprocess.run([
            'python3',
            os.path.join(BASE_DIR, 'idrc_esp_tools/nvs_partition_gen.py'),
            'generate',
            nvs_csv_out.name,
            nvs_partition_out.name,
            str(nvs_partition_size),
        ], capture_output=True, text=True)
        if p.stderr:
            logger.warning(p.stderr)
        p.check_returncode()
        logger.info('Generated new NVS partition')

        # flash NVS partition
        p = subprocess.run([
            'python3', '-m', 'esptool',
            '-p',
            self.usb_port,
            'write_flash',
            str(nvs_partition_offset),
            nvs_partition_out.name,
        ], capture_output=True, text=True)
        if p.stderr:
            logger.warning(p.stderr)
        p.check_returncode()
        logger.info('Flashed new NVS partition')

        # cleanup
        os.unlink(nvs_csv_in.name)
        os.unlink(nvs_csv_out.name)
        os.unlink(nvs_partition_in.name)
        os.unlink(nvs_partition_out.name)
        os.unlink(partition_table_out.name)

        # TODO: start testing
        logger.info('Ready to test!')

    async def run_test_cases(self, include, exclude, tests_list=True, tests_execute=True):
        global exit_code
        tests_passed = True
        include = include or []
        exclude = exclude or []
        if tests_execute:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(
                url=self.usb_port,
                baudrate=self.baudrate,
            )
            self.at = at.AT(
                r=self.reader,
                w=self.writer,
                default_timeout=5,
            )
            try:
                await self.at.TEST.expect_reply(timeout=10)
            except Exception as e:
                logger.error('Hardware did not reply with +TEST acknowledgement')
                logger.error(e)
                exit_code = 1
                return
        if tests_list:
            logger.info('TESTS LIST:')
        for filename in glob.glob(os.path.join(BASE_DIR, 'tests/**/test*.py'), recursive=True):
            module = importlib.machinery.SourceFileLoader('test', filename).load_module()
            if tests_execute and hasattr(module, 'setup'):
                await module.setup(AT=self.at)
            for func_name in dir(module):
                if func_name.startswith('test') and callable(getattr(module, func_name)):
                    if tests_list:
                        logger.info('%s: %s', os.path.basename(filename), func_name)
                    if not tests_execute:
                        continue
                    skip = False
                    for incl in include:
                        if not re.match(incl, func_name):
                            skip = True
                    for excl in exclude:
                        if re.match(excl, func_name):
                            skip = True
                    if skip:
                        logger.warning('[?] %s skipped', func_name)
                        continue
                    try:
                        await getattr(module, func_name)(AT=self.at)
                    except Exception as e:
                        logger.error('[!] %s error %s', func_name, e)
                        tests_passed = False
                    else:
                        logger.info('[x] %s passed', func_name)
            if tests_execute and hasattr(module, 'teardown'):
                await module.teardown(AT=self.at)
        if not tests_execute:
            exit_code = 0
            return
        if tests_passed:
            logger.info('All tests passed, good job!')
            exit_code = 0
        else:
            logger.critical('NOTHING WORKS!!!111')
            exit_code = 1


@click.command()
@click.option('-p', '--port', type=str, help='USB port to open serial to.')
@click.option('-b', '--baudrate', type=int, default=115200, help='Port baudrate.')
@click.option('-i', '--include', multiple=True, help='ONLY execute these test funcs (by func name, regex, multiple).')
@click.option('-x', '--exclude', multiple=True, help='DO NOT execute these test funcs (by func name, regex, multiple).')
@click.option('--tests-list/--no-tests-list', default=True)
@click.option('--tests-execute/--no-tests-execute', default=True)
def main(port, baudrate, include, exclude, tests_list, tests_execute):
    if tests_execute and not port:
        logger.error('--port is required when --tests-execute')
        sys.exit(1)
    runner = SerialTestRunner(usb_port=port, baudrate=baudrate)
    if tests_execute:
        runner.set_nvs_testing_flag()
    asyncio.run(runner.run_test_cases(
        include=include,
        exclude=exclude,
        tests_list=tests_list,
        tests_execute=tests_execute,
    ))

def _main(screen):
    screen.nodelay(0)
    screen.refresh()
    maxy, maxx = screen.getmaxyx()
    info_win = curses.newwin(maxy - 2, maxx // 2 - 2, 0, 1)
    info_win.refresh()
    info_win.scrollok(True)
    info_win.idlok(True)
    info_win.leaveok(True)
    debug_win = curses.newwin(maxy - 2, maxx // 2 - 2, 0, maxx // 2 + 1)
    debug_win.refresh()
    debug_win.scrollok(True)
    debug_win.idlok(True)
    debug_win.leaveok(True)

    handler = CursesHandler(info_win)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    test_logs = logging.getLogger('test')
    test_logs.setLevel(logging.DEBUG)
    test_logs.addHandler(CursesHandler(info_win))

    atlog = logging.getLogger('at')
    atlog.setLevel(logging.DEBUG)
    atlog.addHandler(CursesHandler(debug_win))

    # monkey-patch Click's sys.exit
    _exit = sys.exit
    sys.exit = lambda x: ...
    try:
        main()
    except Exception as e:
        logger.exception(e)
    sys.exit = _exit

    logger.critical('Press any key to exit...')
    screen.getch()
    sys.exit(exit_code)


def run_tester():
    os.makedirs(TMP_DIR, exist_ok=True)
    sys.stdout.write = lambda x, *args, **kwargs: logger.info(x.decode())
    sys.stderr.write = lambda x, *args, **kwargs: logger.info(x.decode())
    curses.wrapper(_main)


if __name__ == '__main__':
    run_tester()
