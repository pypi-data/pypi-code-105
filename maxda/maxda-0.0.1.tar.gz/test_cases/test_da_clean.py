# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 清洗类测试
# author : 
# create_time : 2020/7/18 10:01
# update_time : 2020/7/18 10:01
# copyright : Lavector
# ----------------------------------------------
import unittest

from maxda.analysis.da_clean.clean_interface import CleanFlag
from maxda.analysis.da_clean.water_spam import *
from maxda.analysis.da_clean.navy_judgment import *
from maxda.analysis.da_clean.ads_spam import *
from maxda.analysis.da_clean.ec_spam import *
from maxda.analysis.da_clean.other_spam import *
from maxda.analysis.da_clean.all_text_spam import *
from maxda.analysis.da_clean.unkeyword_spam import *
from maxda.analysis.da_clean.df_distinct import DfDistinct


from maxda.util.panda_tool import PandaTool

from dataset.dataset_config import *


class TestUnitDaClean(unittest.TestCase):

    def test_weibo_water(self):
        content = u'活粉@助力,@助力,@助力,@助力,@助力,@助力,@助力,@助力,@助力4hd44,'
        model_water = WeiboWaterRuleModel()
        result = model_water.process(content)

        self.assertEqual(CleanFlag.YES, result)

    def test_water(self):
        content = {'channel':'weibo','content':u'【178.00】，原件178，满99享优惠。','nickname':''}
        model_water = WaterRuleModel()
        result = model_water.process(content)

        self.assertEqual(CleanFlag.YES, result)

    def test_weibo_add(self):
        content = u'【19.9】宝丽康美 核桃黑芝麻黑豆代餐粉'
        sub_model_ads = WeiboAdsRuleModel()
        result = sub_model_ads.process(content)

        self.assertEqual(CleanFlag.YES, result)

    def test_ec_spam(self):
        spam = EcSpam()
        result = spam.process("救积分")

        self.assertEqual(CleanFlag.YES, result)

    def test_non_chinese_english(self):
        no_ce = NoChineseEnglish()
        result = no_ce.process("234###")

        self.assertEqual(CleanFlag.YES, result)

    def test_text_len(self):
        text_len = TextLen()
        result = text_len.process("k")

        self.assertEqual(CleanFlag.YES, result)

    def test_all_text_spam(self):
        spam = AllTextSpam()
        result = spam.process("转发微博")

        self.assertEqual(CleanFlag.YES, result)

    def test_un_include_keywords(self):
        spam = CleanUnincludedKeyword()
        file_path = os.path.join(example_config_path, "config_clean_no_keyword.xlsx")
        config = {"KeywordExcelPath": file_path}
        spam.load_config_data(**config)

        content = "hello菱歌"
        result = spam.process(content)

        self.assertEqual(CleanFlag.YES, result)

    def test_distinct(self):
        input_file_path = os.path.join(example_test_input_path, "data_distinct.xlsx")
        df_input = PandaTool.read(input_file_path)
        spam_distinct = DfDistinct(input_column="channel,content,datetime",
                                   output_column="tag_clean_dup")

        spam_distinct.process(df_input)


if __name__ == '__main__':
    unittest.main()


