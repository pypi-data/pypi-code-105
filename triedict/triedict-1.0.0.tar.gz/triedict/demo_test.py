# -*- coding: UTF-8 -*-
"""vega FYI 

    @author: vegaviazhang
    @file:demo_test.py
    @time:2021/12/28
"""
from triedict import TrieDict


def main():
    words_list = [
        "糖尿病", "糖尿病一型", "糖尿病二型",
        "慢性肾脏疾病1期", "慢性肾脏疾病2期",
        "高血压", "高血压", "肺组织炎症", "焦虑情绪", "立克次氏体属",
        "AbC"
    ]
    vega_trie = TrieDict()
    vega_trie.init_or_insert_dict(words_list)
    # ['糖尿病一型', '糖尿病', '糖尿病二型', '高血压', '焦虑情绪', '慢性肾脏疾病1期']

    # 1.最大前向匹配
    origin_text = "糖尿病一型糖尿病糖尿病二型高血压焦虑情绪慢性肾脏疾病1期"
    match_list = vega_trie.get_match_words(origin_text)
    print(match_list)

    # 2.判断一个词是否在字典树中
    print(vega_trie.check_exist("abc"))
    # (False, None)


if __name__ == "__main__":
    main()
