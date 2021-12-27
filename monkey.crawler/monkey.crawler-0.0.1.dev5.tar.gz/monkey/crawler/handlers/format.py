# -*- coding: utf-8 -*-

from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler
from datetime import datetime


class FieldStrFormatter(Handler):
    """Formats specified field value using a format spec
    See: 'Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>'_
    """

    def __init__(self, field_name: str, format_spec: str = '', result_field_name: str = None):
        """Initializes the handler.
        :param field_name: the name of the field whose value will be formatted
        :param format_spec: the format specification. If not specified, the format operation behave as a simple string
        conversion.
        :param result_field_name: the name ot the field where the formatted value will be store. If not specified, the
        origin field value will be replaced.
        """
        super().__init__()
        self.field_name = field_name
        self.format_spec = format_spec
        self.result_field_name = field_name if result_field_name is None else result_field_name

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the format operation and store the formatted value in the specified target field.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the formatted value in the target field
        :return: the provided operation code
        """
        rec = record.copy()
        rec[self.result_field_name] = format(record[self.field_name], self.format_spec)
        return rec, op_code


class FieldDatetimeFormatter(Handler):
    """Converts the string value of the specified field into datetime object.
    See: 'Format codes <https://docs.python.org/fr/3/library/datetime.html?highlight=datetime#strftime-strptime-behavior>'_
    """

    def __init__(self, field_name: str, format_spec: str, result_field_name: str = None):
        """Initializes the handler.
        :param field_name: the name of the field whose value will be formatted
        :param format_spec: the format specification.
        :param result_field_name: the name ot the field where the datetime object will be store. If not specified, the
        origin field value will be replaced.
        """
        super().__init__()
        self.field_name = field_name
        self.format_spec = format_spec
        self.result_field_name = field_name if result_field_name is None else result_field_name

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the conversion operation and store the value in the specified target field.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the converted value in the target field
        :return: the provided operation code
        """
        rec = record.copy()
        rec[self.result_field_name] = datetime.strptime(record[self.field_name], self.format_spec)
        return rec, op_code
