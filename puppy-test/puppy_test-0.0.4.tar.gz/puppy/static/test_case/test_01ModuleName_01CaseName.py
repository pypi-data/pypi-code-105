# -*- coding:utf-8 -*-
import unittest, runner
from puppy.core.ddt import data
from puppy.core.ddt import ddt
from puppy.core.api import APIProcessor
from puppy.core.data import ParserTestData
try:
    id=unittest.main.EIO_TEST_ID
except:
    id="-1"
test_file_name = "{}.xml".format(__name__)
test_data = ParserTestData(test_file_name,id).test_data


@ddt
class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*test_data)
    def test(self, case_data):
        APIProcessor(case_data).start()


if __name__ == "__main__":
    unittest.main()