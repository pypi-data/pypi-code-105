# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : LGD
# create_time : 2021/2/20 10:07
# update_time : 2021/2/20 10:07
# copyright : Lavector
# ----------------------------------------------
import os
import unittest
from maxda.analysis.da_tag.label_keyword import KRuleParser
from maxda.analysis.da_tag.label_extract import KeywordSegmentExtractor
from maxda.analysis.da_tag.label_main import LabelDealSimple, LabelDealRelation
from dataset.dataset_config import *

tag_config_path = os.path.join(example_config_path, "config_label_mapping.xlsx")


class TestUnitLabel(unittest.TestCase):
    def test_keyword(self):
        # 0一般测试
        brand_id2keyword = {
            1: "(中国+完成)+(想+要)-(重要+事情)-知道吗|#中华"}
        parser = KRuleParser(brand_id2keyword, build_neg_model=True)
        content = "中国已经完成了最想要12345678知道吗事情，我们还要继续努力人不中华必人胜"
        result = parser.parse(content, return_all=True, direction="both")
        self.assertEqual(len(result), 1)

        # 1.测试双向匹配时可能的错误
        brand_id2keyword = {
            1: "迪奥+999|dior+999|迪奥+666|dior+666"}
        parser = KRuleParser(brand_id2keyword, build_neg_model=True)
        content = "迪奥（dior）口红999礼盒"
        result = parser.parse(content, return_all=True, direction="both")
        self.assertGreaterEqual(len(result), 1)

        # 2.测试距离
        brand_id2keyword = {
            1: "完美日记+哑光唇釉"}
        parser = KRuleParser(brand_id2keyword, build_neg_model=True)
        content = "可以推一下完美日记的反重力唇釉，不显唇纹，也没异味，易涂抹.... 踩一下他的哑光唇釉，有异味"
        result = parser.parse(content, return_all=True, direction="both")
        self.assertEqual(len(result), 0)

        # 3.测试否定词
        brand_id2keyword = {
            1: "@中华"}
        parser = KRuleParser(brand_id2keyword, build_neg_model=True)
        content = "我们还要继续努力人不中华必人胜"
        result = parser.parse(content, return_all=True, direction="both")
        self.assertGreaterEqual(len(result), 1)

        brand_id2keyword = {
            1: "#中华"}
        parser = KRuleParser(brand_id2keyword, build_neg_model=True)
        content = "我们还要继续努力人不中华必人胜"
        result = parser.parse(content, return_all=True, direction="both")
        self.assertEqual(len(result), 0)

    def test_segment_extract(self):

        extractor = KeywordSegmentExtractor()
        config = {"mappingDictPath": tag_config_path}
        extractor.load_config_data(**config)

        # 2.测试分句打标时，数据清洗(大小写)的错误
        content = "感受小金条新色YSL28 ，收获属于我们的显白升级唇妆? 【周震南】"
        title = ""
        data = {"channel": 'weibo', 'content': content, 'title': title}
        input_content, label_texts = extractor.process(data)
        # 只取第一个标签结果
        label_texts = label_texts[0]['content']
        self.assertGreaterEqual(len(label_texts), 1)

        # 3.测试分句
        content = "质地也很高级！丝绒哑光我爱了"
        title = ""
        data = {"channel": 'weibo', 'content': content, 'title': title}
        input_content, label_texts = extractor.process(data)
        # 只取第一个标签结果
        label_texts = label_texts[0]['content']
        # print(label_texts)
        self.assertEqual(len(label_texts), 0)

    def test_label(self):
        config = {"mappingDictPath": tag_config_path}

        simple_object = LabelDealSimple()
        simple_object.load_config_data(**config)

        relation_object = LabelDealRelation()
        relation_object.load_config_data(**config)

        content = "也是秋冬必备的颜色之一"
        title = "纪梵希绝美新色，颜色漂亮呀"
        data = {"channel": 'redbook', 'content': content, 'title': title}

        s_last_result1 = simple_object.process(data)
        s_last_result2 = relation_object.process(data)

        self.assertEqual(len(s_last_result1[-1][1]), 2)
        # TODO 不分句功能，不需要扩展，所有标签都是有效的
        self.assertEqual(len(s_last_result1[-1][0]), 1)

        self.assertEqual(len(s_last_result2[-1][1]), 2)
        # TODO 不分句功能，有时需要扩展，因此有需要标签要删除
        self.assertEqual(len(s_last_result2[-1][0]), 0)

    def test_business(self):
        """
        测试业务类
        :return:
        """
        config = {"mappingDictPath": tag_config_path}

        simple_object = LabelDealSimple()
        simple_object.load_config_data(**config)

        # relation_object = LabelDealRelation()
        # relation_object.load_config_data(**config)

        content = "也是秋冬必备的颜色之一"
        title = "纪梵希绝美新色，颜色漂亮呀"
        data = {"channel": 'nosetime', 'content': content, 'title': title}

        s_last_result = simple_object.process(data)
        # r_last_result = relation_object.process(data)

        # 2.测试特殊渠道处理, 电商类渠道title不作距离限制了
        title = "兰蔻菁纯123456789哑光口红也是颜色之一"
        content = "七宗罪123456唇釉绝美新色"
        data = {"channel": 'jd', 'content': content, 'title': title}

        s_last_result = simple_object.process(data)
        # print(s_last_result[0], s_last_result[2])
        self.assertEqual(len(s_last_result[0]), 3)

        # 3.测试购买类
        # relation_object = LabelDealRelation()
        # config = {"mappingDictPath": os.path.join(example_config_path, "config_label_mapping_purchase.xlsx")}
        # relation_object.load_config_data(**config)
        #
        # title = "口红"
        # content1 = "抽奖七宗罪唇釉绝美新色一,用了"
        # data = {"channel": 'jd', 'content': content1, 'title': title}
        #
        # s_last_result = relation_object.process(data)
        # 命中标签
        # self.assertGreaterEqual(len(s_last_result[0]), 1)
        #
        # content2 = "抽奖七宗罪唇釉绝美新色一"
        # data = {"channel": 'jd', 'content': content2, 'title': title}
        #
        # s_last_result = relation_object.process(data)
        # 无标签
        # self.assertEqual(len(s_last_result[0]), 0)

    def test_segment_expand(self):
        """
        测试分句扩展
        :return:
        """
        config = {"mappingDictPath": tag_config_path}

        relation_object = LabelDealRelation()
        relation_object.load_config_data(**config)

        title = "完美日记小金钻也是秋冬必备的颜色之一"
        content = "欧莱雅粉管绝美新色，秋冬颜色。秋冬颜色漂亮。花西子同心锁口红自然呀, 欧诗漫秋自然,欧诗漫秋高端。真高冷呀"
        data = {"channel": 'nosetime', 'content': content, 'title': title}

        # s_last_result = simple_object.process(data)
        s_last_result = relation_object.process(data)
        # print(s_last_result[0], s_last_result[2])
        # [(103, 348), (103, 55), (274, None), (235, 289), (235, 77), (103, 236)]
        # [{235: {'欧莱雅粉管'}, 103: {'花西子同心锁口红'}, 274: {'完美日记小金钻'}}, {289: {'秋冬颜色'}, 77: {'颜色漂亮'}, 55: {'自然'}, 348: {'高端'}, 236: {'高冷'}}]

        self.assertEqual(len(s_last_result[0]), 6)
