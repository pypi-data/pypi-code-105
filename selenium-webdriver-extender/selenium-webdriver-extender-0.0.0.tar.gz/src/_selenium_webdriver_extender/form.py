"""
Module for the static class Form, used for inserting and deleting string objects into web forms.
"""

from typing import Union

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class Form:
    """
    Class for handling form text input and clearing form.
    """
    @staticmethod
    def clear_input(driver: WebDriver, input_element: WebElement) -> None:
        """
        Method clears data in the form.

        Args:
            driver: Instance of driver used.
            input_element: Form element to insert data into.
        """
        # select text input and just loop with backspace button a bunch of times to delete whatever is set in CRM
        driver.execute_script('arguments[0].click()', input_element)
        for _ in range(len(input_element.get_attribute("value"))):  # Delete all characters
            input_element.send_keys(Keys.BACKSPACE)

    @staticmethod
    def insert_in_input(input_element: any, value_to_insert: Union[str, int, float]) -> None:
        """
        Method inserts value into form/element.

        Args:
            input_element: Element to insert value.
            value_to_insert: Value to insert into form element.
        """
        input_element.send_keys(value_to_insert)

    @staticmethod
    def clear_and_insert(driver: WebDriver, input_element: any, value_to_insert: Union[str, int, float]) -> None:
        """
        Method clears input element and inserts value.

        Args:
            driver (WebDriver): Instance of driver used.
            input_element (any): Form element to insert data into.
            value_to_insert (str or int or float): Value to insert into form element.
        """
        Form.clear_input(driver, input_element)
        Form.insert_in_input(input_element, value_to_insert)
