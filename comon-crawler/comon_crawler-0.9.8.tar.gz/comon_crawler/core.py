import time
import logging
from enum import Enum
from typing import Union

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        ElementClickInterceptedException,
                                        WebDriverException)


class Selector(Enum):
    by_class_name = By.CLASS_NAME
    by_id = By.ID
    by_name = By.NAME
    by_xpath = By.XPATH
    by_tag_name = By.TAG_NAME


class Event(Enum):
    be_located = EC.presence_of_element_located
    be_visible = EC.visibility_of_element_located
    be_invisible = EC.invisibility_of_element_located
    be_clicked = EC.element_to_be_clickable


docker_remote_options = {
    'command_executor': "http://selenium:4444/wd/hub",
    'desired_capabilities': DesiredCapabilities.CHROME
}


class CrawlerCore:
    """
    CRAWLER CORE CLASS
    """
    remote_options = docker_remote_options
    base_options = ChromeOptions()
    base_options.headless = True
    base_options.add_argument('--window-size=1280x1696')
    base_options.add_argument('--no-sandbox')  # # Bypass OS security model
    base_options.add_argument('start-maximized')

    def __init__(self, remote: bool = False, debug: bool = False):
        self.remote = remote
        self.debug = debug
        self.driver = None

    def _init_driver(self) -> None:
        self.driver = self._get_driver()

    def _get_driver(self) -> WebDriver:
        if self.remote:
            return webdriver.Remote(**self.remote_options, options=self.base_options)
        if self.debug:
            self.base_options.headless = False
        return webdriver.Chrome(options=self.base_options)

    def start(self) -> None:
        # инициализируем драйвер явныи образом в момент запуска краулера
        self._init_driver()
        # self.driver.get(self.url)

    def make_element_visible(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].style.display = 'block';", element)

    def change_element_class_name(self, element: WebElement, new_name: str) -> None:
        self.driver.execute_script(f"arguments[0].setAttribute('class', '{new_name}')", element)

    def open_page_in_new_tab(self, url: str) -> None:
        # открываем вкладку
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        self.driver.get(url)

    def wait_element(self,
                     selector: Selector,
                     value: str,
                     condition: Event = Event.be_located) -> WebElement:
        wait = WebDriverWait(self.driver, 15)
        return wait.until(condition.value((selector.value, value)))

    @classmethod
    def wait_select_element(cls, element: WebElement) -> Select:
        return Select(element)

    @classmethod
    def choice_select_element_value(cls, select: Select, value: Union[str, int]) -> WebElement:
        return select.select_by_value(value)

    @classmethod
    def send_keys(cls, element: WebElement, value: Union[str, int]) -> None:
        element.send_keys(value)

    @classmethod
    def click_on_element(cls, element: WebElement) -> None:
        element.click()

    def element_is_exists(self, selector: Selector, value: str) -> bool:
        try:
            self.driver.find_element(selector.value, value)
        except NoSuchElementException:
            return False
        return True

    def stop(self) -> None:
        self.driver.quit()

    @classmethod
    def wait(cls, seconds: int = 3) -> None:
        time.sleep(seconds)


def attempted_crawling(attempts: int):
    # декоратор увеличения попыток краулинга
    def actual_decorator(func):

        def wrapper(*args, **kwargs):
            attempt = 0
            self = args[0]
            while attempt < attempts:
                logging.warning(f'ATTEMPT# {attempt}')
                try:
                    return func(*args, **kwargs)
                except (NoSuchElementException,
                        TimeoutException,
                        AttributeError,
                        WebDriverException,
                        ElementClickInterceptedException) as e:
                    logging.warning(e)
                    self.stop()
                    attempt += 1
            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def logg_func_execution(func):
    def echo_func(*func_args, **func_kwargs):
        logging.warning(f'{func.__name__}: in process')
        result = func(*func_args, **func_kwargs)
        logging.warning(f'{func.__name__}: done')
        return result

    return echo_func
