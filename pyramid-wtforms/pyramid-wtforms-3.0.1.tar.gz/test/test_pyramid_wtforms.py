import unittest


class TestPyramidWTForms(unittest.TestCase):

    def test_pyramid_wtforms_should_have_essential_elements(self):
        import pyramid_wtforms
        essential_elements = [i for i in dir(pyramid_wtforms)
                              if i[0].isupper()]
        self.assertEqual(
            ['BooleanField', 'DateField', 'DateTimeField', 'DateTimeLocalField',
             'DecimalField', 'DecimalRangeField', 'EmailField', 'Field', 'FieldList',
             'FileField', 'Flags', 'FloatField', 'Form', 'FormField', 'HiddenField',
             'IntegerField', 'IntegerRangeField', 'Label', 'MonthField', 'MultipleCheckboxField',
             'MultipleFileField', 'MultipleFilesField', 'PasswordField', 'RadioField',
             'SearchField', 'SecureForm', 'SelectField', 'SelectFieldBase', 'SelectMultipleField',
             'StringField', 'SubmitField', 'TelField', 'TextAreaField', 'TimeField', 'URLField',
             'ValidationError'],
            essential_elements
        )
