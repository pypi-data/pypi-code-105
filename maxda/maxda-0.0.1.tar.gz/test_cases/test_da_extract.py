# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 测试抽取类相关功能
# author : 
# create_time : 2020/7/18 15:44
# update_time : 2020/7/18 15:44
# copyright : Lavector
# ----------------------------------------------
import unittest

from maxda.analysis.da_extract.age_format import *
from maxda.analysis.da_extract.city_rank import *
from maxda.analysis.da_extract.gender_format import *
from maxda.analysis.da_extract.number_format import *
from maxda.analysis.da_extract.text_format import *
from maxda.analysis.da_extract.user_tag import *


class TestUnitDaExtract(unittest.TestCase):
    def test_age_format(self):
        from datetime import datetime

        age_format = AgeFormat()
        input_date ={'age':"2000年12月26日"}
        input_year = int(input_date['age'].split("年")[0])
        result = age_format.process({'age':"2000年12月26日"})

        now_year = int(datetime.now().strftime("%Y"))
        epoch_year = now_year - input_year + 1
        self.assertEqual(epoch_year, result)

    def test_age_level(self):
        age_level = AgeLevelFormat()
        result = age_level.process(19)
        self.assertEqual(result, 2)

    def test_city_rank(self):
        city_rank = CustomCityRank()
        result = city_rank.process({'city': '重庆'})

        self.assertEqual(result[0], '重庆')
        self.assertEqual(result[1], '新一线')

    def test_format_datetime(self):
        datetime_format = DateTimeFormat()

        datetime_string = "二○一七年六月二十日"
        result = datetime_format.process(datetime_string)
        self.assertEqual(result, '2017-06-20')

        datetime_string = "2019年4月5日 18:21"
        result = datetime_format.process(datetime_string)
        self.assertEqual(result, '2019-04-05')

        datetime_string = "2019/06/02 22:50:00.000"
        result = datetime_format.process(datetime_string)
        self.assertEqual(result, '2019-06-02')

        datetime_string = "2019年06月02日22:50"
        result = datetime_format.process(datetime_string)
        self.assertEqual(result, '2019-06-02')

        datetime_string = "2019-10-11 22:13:00"
        result = datetime_format.process(datetime_string)
        self.assertEqual(result, '2019-10-11')

        datetime_string = "5772518427"
        result = datetime_format.process(datetime_string)
        self.assertIsNone(result, result)

    def test_gender_format(self):
        gender_format = GenderFormat()
        result = gender_format.process({'gender': '', 'nickname': '宅男'})

        self.assertEqual(result, '男')

    def test_number_format(self):
        int_format = IntFormat()
        result = int_format.process("23.23")
        self.assertEqual(result, 23)

        float_format = FloatFormat()
        result = float_format.process("23.2390")
        self.assertEqual(result, 23.24)

    def test_text_format(self):
        text = "中國好"
        t = Tradition2Simple()
        result = t.process(text)

        self.assertEqual(result, "中国好")

    def test_user_tag(self):
        classify = '食品饮料'
        user_tag = UserTag(classify)
        result = user_tag.process({'channel': 'weibo', 'userid': '2137888361'})
        self.assertEqual(result, "bgc")

        result = user_tag.process({'channel': 'weibo', 'userid': '1749159601'})
        self.assertEqual(result, "star")

        result = user_tag.process({'channel': 'weibo', 'userid': '1005053155899501'})
        self.assertEqual(result, "ugc")


if __name__ == '__main__':
    unittest.main()
