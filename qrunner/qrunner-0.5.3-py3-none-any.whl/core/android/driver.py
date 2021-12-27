import os
import time

import allure
import uiautomator2 as u2
from qrunner import Browser, logger
from qrunner.utils.data import get_time


class Driver(object):
    _instance = {}

    def __new__(cls, serial_no=None):
        if not serial_no:
            serial_no = Browser.serial_no
        if serial_no not in cls._instance:
            cls._instance[serial_no] = super().__new__(cls)
        return cls._instance[serial_no]

    def __init__(self, serial_no=None):
        if not serial_no:
            serial_no = Browser.serial_no
        logger.info(f'启动 android driver for {serial_no}')
        self.d = u2.connect(serial_no)

    @classmethod
    def get_instance(cls, serial_no=None):
        """Create singleton"""
        if serial_no not in cls._instance:
            logger.info(f'[{serial_no}] Create android driver singleton')
            return Driver(serial_no).d
        return Driver._instance[serial_no].d

    # @classmethod
    # def get_remote_instance(cls, server_url, token):
    #     device = Device(server_url, token)
    #     d = u2.connect(device.get_device())
    #     return d, device

    def uninstall_app(self, pkg_name=None):
        if not pkg_name:
            pkg_name = Browser.pkg_name
        logger.info(f'卸载应用: {pkg_name}')
        self.d.app_uninstall(pkg_name)

    def install_app(self, apk_path, is_new=False):
        if is_new:
            self.uninstall_app(Browser.pkg_name)
        logger.info(f'安装应用: {apk_path}')
        self.d.app_install(apk_path)

    def start_app(self, pkg_name=None):
        if not pkg_name:
            pkg_name = Browser.pkg_name
        logger.info(f'启动应用: {pkg_name}')
        self.d.app_start(pkg_name)

    def stop_app(self, pkg_name=None):
        if not pkg_name:
            pkg_name = Browser.pkg_name
        logger.info(f'退出应用: {pkg_name}')
        self.d.app_stop(pkg_name)

    def force_start_app(self, pkg_name=None):
        if not pkg_name:
            pkg_name = Browser.pkg_name
        logger.info(f'强制启动应用: {pkg_name}')
        self.d.app_start(pkg_name, stop=True)

    def delete(self):
        logger.info('点击一次退格键')
        self.d.press('delete')

    # 有时候clear_text方法不管用，可以尝试该方法
    def clear(self, num=10):
        logger.info('清空输入框: 通过点击10次退格键实现')
        for i in range(num):
            self.delete()

    def click(self, x, y):
        self.d.click(x, y)

    def handle_alert(self, alert_list: list):
        with self.d.watch_context() as ctx:
            for alert in alert_list:
                ctx.when(alert).click()
            ctx.wait_stable()

    def double_click(self, x, y):
        self.d.double_click(x, y)

    def long_click(self, x, y):
        self.d.long_click(x, y)

    def swipe(self, sx, sy, ex, ey):
        self.d.swipe(sx, sy, ex, ey)

    def swipe_left(self, scale=0.9):
        self.d.swipe_ext('left', scale=scale)

    def swipe_right(self, scale=0.9):
        self.d.swipe_ext('right', scale=scale)

    def swipe_up(self, scale=0.8):
        self.d.swipe_ext('up', scale=scale)

    def swipe_down(self, scale=0.8):
        self.d.swipe_ext('down', scale=scale)

    def drag(self, sx, sy, ex, ey):
        self.d.drag(sx, sy, ex, ey)

    def screenshot(self, name):
        self.d.screenshot(name)

    def upload_pic(self, filename):
        self.screenshot('tmp.png')
        allure.attach.file(
            'tmp.png',
            attachment_type=allure.attachment_type.PNG,
            name=f'{filename}-{get_time()}'
        )
        os.remove('tmp.png')

    def input_text(self, text):
        self.d.clear_text()
        self.d.send_keys(text)
        self.d.send_action('search')
        self.d.set_fastinput_ime(False)

    def input_password(self, text):
        self.d(focused=True).set_text(text)

    @property
    def page_content(self):
        return self.d.dump_hierarchy()

    @property
    def window_size(self):
        return self.d.window_size()

    def back(self):
        self.d.press('back')

    def search(self):
        self.d.press('search')

    def enter(self):
        self.d.press('enter')




