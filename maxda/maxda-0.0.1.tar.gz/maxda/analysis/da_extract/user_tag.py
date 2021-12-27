# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 提取用户类型 PGC/UGC/BGC
# author : 
# create_time : 2020/6/30 10:23
# update_time : 2020/6/30 10:23
# copyright : Lavector
# ----------------------------------------------
from maxda.analysis.analysis_interface import *
from maxda.util.mysql_util import LavwikiReader
import pandas as pd


class UserTag(RowInterface):
    def __init__(self, classify, default_value=None):
        super(UserTag, self).__init__(default_value)

        tag_df = LavwikiReader.get_as_df("lav2bgc_star")[
            ['classify', 'channel', 'userid', 'user_tag', 'brand']]
        tag_bgc_df = tag_df[(tag_df['classify'] == classify) | (tag_df['classify'] == 'currency')]
        tag_star_df = tag_df[tag_df['classify'] == 'personal']
        tag_pgc_df = tag_df[(tag_df['classify'] != 'personal') & (tag_df['classify'] != classify)].loc[:,
                     ('classify', 'channel', 'userid', 'user_tag')]
        tag_pgc_df.loc[:, 'user_tag'] = 'pgc'
        # 下面这四行是为了去除重复的userID
        bgc_list = list(tag_bgc_df['userid'])
        tag_pgc_df['kk'] = tag_pgc_df.apply(lambda x: x['userid'] in bgc_list, axis=1)
        tag_pgc_df = tag_pgc_df[tag_pgc_df['kk'] == False]
        self.tag_dict = {}
        this_tag_df = pd.concat([tag_bgc_df, tag_star_df, tag_pgc_df], sort=False)
        for a, b in this_tag_df.groupby('channel'):
            b.index = b['userid']
            self.tag_dict[a] = b['user_tag'].to_dict()

        self.redbook_brand_list = [i.lower() for i in list(
            tag_df[tag_df['channel'] == 'redbook'][tag_df[tag_df['channel'] == 'redbook']['classify'] == classify][
                'brand'])]
        self.redbook_pgc_list = ['qq.com', '163.com', '126.com', 'icloud.com', 'htomail.com', 'xzwh.com',
                                 'yahoo.com', 'gmail.com', '邮箱', '美妆博主', '原创博主', '时尚博主', '店铺', '连锁店',
                                 '店主', 'b站', 'wb', '微博', 'ins', '同名', '干货', '分享', '直播', '搬运', '金冠薯']
        self.weibo_pgc_list = ['自媒体', '官方网站', '官方微博', '学者', '作家', '专家', '教授', '导师', '医师', '创始人', '主理人', '达人', '博主',
                               '主编', '编辑', '编剧', '漫画家', '撰稿人', '电竞选手', '游戏选手', '评论人', '影评人', '剧评人', '股评师', '股评人',
                               '优秀回答者', '顾问', '测评', '评测', '安利', '投资', 'vlog', '欢迎投稿', '答主', '问答', '原创', '头条文章作者',
                               '游戏视频自媒体', '医生', '美妆博主', '美食博主', '时尚博主', '摄影博主', '中国区总代理', '经销商']
        self.weibo_star_list = ['反黑站']
        self.tiktok_pgc_list = ['商业合作', '合作', '商务', '联系', '全网同名', '说明来意', '注明来意', '邮箱',
                                '导演', '制作人', '造型师', '专家', '导师', '医生', '博主', '创作者', '成员', '官方',
                                'qq.com', '163.com', '126.com', 'icloud.com', 'htomail.com', 'xzwh.com',
                                'yahoo.com', 'gmail.com', 'vx', 'wx', '微信', '酷狗', 'b站', 'q音', '网易云',
                                'vb', '微博', '微吧', '围脖', 'wb', 'weibo', ]

    def func_redbook(self, data, judge_text, user_tag='ugc'):
        # 认证
        authentication = data['authentication']
        if authentication == '蓝标':
            user_tag = 'pgc'
            if list(filter(lambda x: x in data['nickname'], self.redbook_brand_list)):
                user_tag = 'bgc'
                return user_tag
            return user_tag
        if authentication == '红标':
            user_tag = 'pgc'
            return user_tag
        # 粉丝
        if str(data['fans']).isnumeric():
            ss = int(data['fans'])
            if ss <= 1000 and user_tag != 'pgc':
                user_tag = 'ugc'
            else:
                user_tag = 'pgc'
                return user_tag
        # 简介、昵称、用户标签
        if list(filter(lambda x: x in judge_text, self.redbook_pgc_list)):
            user_tag = 'pgc'
        return user_tag

    def func_tiktok(self, data, judge_text, user_tag='ugc'):
        # 粉丝
        if str(data['fans']).isnumeric():
            ss = int(data['fans'])
            if ss <= 5000 and user_tag != 'pgc':
                user_tag = 'ugc'
            else:
                user_tag = 'pgc'
                return user_tag
        # 认证
        if data['authentication'] == '红标' or data['authentication'] == '蓝标':
            user_tag = 'pgc'
            return user_tag
        # 简介、昵称、用户标签
        if list(filter(lambda x: x in judge_text, self.tiktok_pgc_list)):
            user_tag = 'pgc'

        return user_tag

    def func_weibo(self, data, judge_text, user_tag='ugc'):
        # 粉丝
        if str(data['fans']).isnumeric():
            ss = int(data['fans'])
            if ss <= 3000 and user_tag != 'pgc':
                user_tag = 'ugc'
            else:
                user_tag = 'pgc'
                return user_tag
        # 认证
        if data['authentication'] == '黄标' or data['authentication'] == '蓝标':
            user_tag = 'pgc'
            return user_tag
        # 简介、昵称、用户标签
        if list(filter(lambda x: x in judge_text, self.weibo_star_list)):
            user_tag = 'star'
            return user_tag
        if list(filter(lambda x: x in judge_text, self.weibo_pgc_list)):
            user_tag = 'pgc'

        return user_tag

    def distribute(self, data, **params):
        '''
        分布处理三个平台的数据
        :param data: 字典类型一行数据
        :param params:
        :return:
        '''
        judge_column_name_list = ['fans', 'authentication', 'introduce', 'user_label', 'nickname']
        for column_name in judge_column_name_list:
            if column_name not in data:
                data[column_name] = ''
        judge_text = '.'.join([str(data[i]) for i in judge_column_name_list[1:] if data[i]]).lower()
        channel_dict = {'redbook': self.func_redbook, 'weibo': self.func_weibo, 'tiktok': self.func_tiktok}
        return channel_dict[data['channel']](data, judge_text)

    def process(self, data, **params):
        """
        判断用户类别
        """
        user_tag = 'ugc'  # 默认为ugc
        if data['channel'] in self.tag_dict and data['userid'] in self.tag_dict[data['channel']]:
            user_tag = self.tag_dict[data['channel']][str(data['userid'])]
        if data['channel'] in ['redbook', 'weibo', 'tiktok'] and user_tag not in ['bgc', 'star']:
            user_tag = self.distribute(data)
        # TODO 默认给定ugc
        return user_tag


if __name__ == '__main__':
    classify = '保健品'
    # classify = '皮肤美容大健康'
    user_tag = UserTag(classify)
    # data = {'channel': 'weibo', 'userid': '2137888361'} # 零食 bgc
    # data = {'channel': 'weibo', 'userid': '2301502660'}  # 保健品 bgc
    # data = {'channel': 'weibo', 'userid': '3339573404'} # 明星 star
    data = {'channel': 'tiktok', 'userid': '61111281471',
            'url': 'www.iesdouyin.com/share/user/61111281471?sec_uid=MS4wLjABAAAAwkg8LvZQSWj45ynHDCimtxuyry_9iqSMttrxFeK_d14',
            'nickname': '晁然然然然', 'gender': '女', 'city': '강남구',
            'user_label': '. 起个大早听鸟叫 \nwb. 晁然然然然\n每周六深夜直播聊聊天～\n工作联系 chaorannnn@sina.com', 'fans': 3535072,
            'authentication': '红标'}
    # 皮肤美容大健康 bgc
    # print(user_tag.process("55730319c2bdeb4d2c0976f9")) # KOL

    print(user_tag.process(data))  # start
    # print(user_tag.process("630832970388"))  # ugc
