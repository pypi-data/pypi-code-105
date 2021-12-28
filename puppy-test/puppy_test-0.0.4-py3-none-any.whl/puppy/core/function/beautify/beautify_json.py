# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: beautify json
"""
import re
from ..parse.json_parse import JsonParse


class BeautifyJson(object):
    __blank_re = re.compile(r"\s")
    __blank = chr(12288)
    __single = 2

    def __init__(self, json: str):
        """
        待美化的json字符串
        :param json:
        """
        self.__json = json
        if not JsonParse.is_correct_json(json):
            raise Exception("{}不是正确的json字符串".format(json))
        self.__beautified_json = ""

    def beautify(self):
        """
        获得美化后的json字符串
        :return:
        """
        # 空白字符
        # 空白字符所有数量
        number_of_blank = 0
        # 单级空白字符数量
        json_list = list(self.__json)
        double_quotation_marks = False
        backslash = False
        for letter in json_list:
            if BeautifyJson.__blank_re.fullmatch(letter) and not double_quotation_marks:
                continue
            if letter == "\\":
                backslash = not backslash
                continue
            if letter == '"' and not backslash:
                double_quotation_marks = not double_quotation_marks
                self.__beautified_json += '"'
                continue
            if letter in ['{', '['] and not double_quotation_marks:
                self.__beautified_json += "{}\n".format(letter)
                number_of_blank += BeautifyJson.__single
                self.__beautified_json += BeautifyJson.__blank * number_of_blank
                continue
            if letter == ':' and not double_quotation_marks:
                self.__beautified_json += ": "
                continue
            if letter in [']', '}'] and not double_quotation_marks:
                number_of_blank -= BeautifyJson.__single
                self.__beautified_json += "\n{}{}".format(BeautifyJson.__blank * number_of_blank, letter)
                continue
            if letter == ',' and not double_quotation_marks:
                self.__beautified_json += ",\n{}".format(BeautifyJson.__blank * number_of_blank)
                continue
            self.__beautified_json += letter
        return self.__beautified_json
