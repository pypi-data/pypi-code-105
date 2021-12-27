import inspect
import threading
from qrunner import Browser
from qrunner.utils.exceptions import ElementTypeError
from qrunner.utils.log import logger
from qrunner.core.ios.driver import relaunch_wda, Driver
from selenium.common.exceptions import NoSuchElementException

# 初始化driver
driver = Driver(Browser.serial_no)
d = Driver.get_instance(Browser.serial_no)

# 支持的定位方式
LOC_LIST = ['name', 'nameContains', 'label', 'labelContains', 'value', 'valueContains', 'className', 'xpath']

# 默认支持的弹窗处理
DEFAULT_ALERTS = [
    '使用App时允许',
    '允许',
    '始终允许'
]


# 根据不同定位方式进行点击
def click(loc):
    timeout = 2
    try:
        if '//' in loc:
            d.xpath(loc).click(timeout=timeout)
        else:
            d(name=loc).click(timeout=timeout)
    except Exception:
        pass


# 多线程处理异常弹窗
def handle_alert():
    alert_list = []
    alert_list.extend(DEFAULT_ALERTS)
    alert_list.extend(Browser.alert_config)
    thread_list = []
    for alert in alert_list:
        t = threading.Thread(target=click, args=(alert,))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()


# IOS元素定义
class Element(object):
    def __init__(self, *args, **kwargs):
        self._index = kwargs.pop('index', 0)

        for k, v in kwargs.items():
            if k not in LOC_LIST:
                raise ElementTypeError(f'不支持的定位方式: {k}')

        if not kwargs:
            raise ElementTypeError(f'请指定定位方式: {args}')

        self.xpath = kwargs.get('xpath', '')
        self._kwargs = kwargs
        self._element = None

    @relaunch_wda
    def find_element(self, retry=3, timeout=3):
        self._element = d.xpath(self.xpath) if \
            self.xpath else d(**self._kwargs)[self._index]
        while not self._element.wait(timeout=timeout):
            if retry > 0:
                retry -= 1
                logger.warning(f'重试 查找元素： {self._kwargs}')
                handle_alert()
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'【{caller.function}:{caller.lineno}】未找到元素 {self._kwargs}')
                return None
        return self._element

    @relaunch_wda
    def _get_element(self, retry=5, timeout=3):
        element = self.find_element(retry=retry, timeout=timeout)
        if element is None:
            driver.upload_pic(list(self._kwargs.values())[0])
            raise NoSuchElementException(f'未定位到元素: {self._kwargs}')
        return element

    @relaunch_wda
    def attr(self, name):
        logger.info(f'元素 {self._kwargs},{self._index}-{name} 属性:')
        element = self._get_element(retry=0)
        info_dict = {
            'info': element.info,
            'count': element.count(),
            'name': element.name,
            'label': element.label,
            'value': element.value,
            'className': element.className,
            'visible': element.visible,
            'bounds': element.bounds,
            'text': element.text
        }
        _info = info_dict.get(name)
        logger.info(_info)
        return _info

    # 用于常见分支场景判断
    @relaunch_wda
    def exists(self, timeout=1):
        logger.info(f'元素 {self._kwargs},{self._index} 是否存在:')
        _exist = self.find_element(retry=0, timeout=timeout) is not None
        logger.info(_exist)
        return _exist

    @relaunch_wda
    def click(self, flag=True):
        logger.info(f'点击元素: {self._kwargs},{self._index}')
        element = self._get_element()
        if flag:
            handle_alert()
        element.click()

    @relaunch_wda
    def click_exists(self, timeout=1):
        if self.exists(timeout=timeout):
            self.click()

    @relaunch_wda
    def input(self, text, clear=True):
        logger.info(f'输入框 {self._kwargs},{self._index} 输入: {text}')
        element = self._get_element()
        if clear:
            element.clear_text()
        element.set_text(text)
        logger.info('输入成功')

    @relaunch_wda
    def scroll(self):
        self._get_element().scroll()

    @relaunch_wda
    def swipe_left(self):
        self._get_element().swipe("left")

    @relaunch_wda
    def swipe_right(self):
        self._get_element().swipe("right")

    @relaunch_wda
    def swipe_up(self):
        self._get_element().swipe("up")

    @relaunch_wda
    def swipe_down(self):
        self._get_element().swipe("down")

    @relaunch_wda
    def child(self, *args, **kwargs):
        return self._get_element().child(*args, **kwargs)




