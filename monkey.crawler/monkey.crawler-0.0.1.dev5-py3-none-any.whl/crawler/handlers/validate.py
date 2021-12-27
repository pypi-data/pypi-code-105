# -*- coding: utf-8 -*-
# TODO: Field validation against min, max, expression evaluation

from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler, InputError


class ValidationFieldError(InputError):

    def __init__(self, record_info, violations):
        details = '\n\t'.join(violations)
        super().__init__(record_info, f'Validation errors:{details}')
        self.violations = violations


class FieldValidator(Handler):
    """Checks if specified fields verify specific conditions"""

    def __init__(self, field_names: set[str]):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        """
        super().__init__()
        self.field_names = field_names

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the validation check on target fields from the provided record.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: the provided record
        :return: the provided operation code
        :raise MissingRequiredFieldError: if any required field is missing or empty.
        """
        violations = []
        for field_name in self.field_names:
            violation = self.validate(record, field_name)
            if violation:
                violations.append(violation)
        if len(violations):
            raise ValidationFieldError(record, violations)
        else:
            return record, op_code

    def validate(self, record: dict, field_name:str ):
        """Performs the validation check on the specified field from the provided record.
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        raise NotImplementedError('Not yet implemented')


class RequiredFieldValidator(FieldValidator):
    """Checks if required fields are provided and if they are not not empty."""

    def __init__(self, field_names: set[str], accept_empty: bool = True):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param accept_empty: indicates if empty value are accepted or not
        """
        super().__init__(field_names)
        self.accept_empty = accept_empty

    def validate(self, record: dict, field_name):
        """Performs the validation check on the specified field from the provided record.
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        violation = None
        try:
            value = record.get(field_name)
            if not (self.accept_empty or bool(value)):
                violation = f'Required field \'{field_name}\' is empty<.'
        except KeyError:
            violation = f'Required field \'{field_name}\' is missing.'
        return violation



