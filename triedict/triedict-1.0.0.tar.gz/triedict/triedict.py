# -*- coding: UTF-8 -*-
"""vega FYI 最大前向匹配的原理及其实用实现
    可以debug看下，就是通过空间换时间
    Trie，前缀树/字典树  搜索时间复杂度为O(l)  l为字符串长度。
    Google的开源实现：https://github.com/google/pygtrie

    @author: vegaviazhang
    @file:triedict.py
    @time:2021/10/04
"""
from typing import Union, List, Tuple, Set, Optional


class TrieDict:
    def __init__(self, ignored_chars: Union[str, List, Tuple, Set] = None, stop_word=False):
        if ignored_chars is None:
            ignored_chars = "/"
        self.ignored_chars = ignored_chars
        self.stop_word = stop_word
        self.trie = {}  # 关键字典树

    def init_or_insert_dict(self, items: Union[List, Tuple, Set], ) -> None:
        """vega FYI 初始化字典树或者扩充字典树
        """
        # TODO 中文符号处理  ->可以参考transformers中的中文处理包
        for item in items:
            item = item.strip()
            if not item:
                continue
            curr_trie = self.trie
            item = item.lower() if self.stop_word else item
            for sub_char in item:
                if sub_char not in self.ignored_chars:
                    curr_trie = curr_trie.setdefault(sub_char, {})
            curr_trie["whole_word"] = item

    def get_match(self, text: str) -> Tuple[Union[None, str], int]:
        """vega FYI 从头开始匹配，匹配到一个就返回，相当于 re.match
            从text的开始往后匹配,返回匹配到的内容和序号
        """
        curr_trie, longest_match, offset = self.trie, None, 0
        if not text:
            return longest_match, offset
        text = text.lower() if self.stop_word else text
        for idx, sub_char in enumerate(text):
            if sub_char not in self.ignored_chars:
                if sub_char not in curr_trie:
                    return longest_match, offset
                curr_trie = curr_trie[sub_char]
                if "whole_word" in curr_trie:
                    longest_match, offset = curr_trie["whole_word"], idx + 1
        return longest_match, offset

    def check_exist(self, text: str) -> Tuple[bool, Optional[str]]:
        """vega FYI 判断text是否在字典树中
            从text的idx 0往后匹配,如果没有匹配到，
            接着从1开始匹配，如果匹配到了，
            假设长度为3，继续从索引3开始匹配
        """
        word_exist_bool, first_match_word = False, None
        text = text.lower() if self.stop_word else text
        text_len = len(text)
        start_idx = 0
        while start_idx <= text_len - 1:
            sub_text = text[start_idx:]
            temp_word, curr_trie = "", self.trie
            # print(len(self.trie))  # vega FYI 这不用copy也行
            for sub_char in sub_text:
                if sub_char not in self.ignored_chars:
                    if sub_char not in curr_trie:
                        break
                    curr_trie = curr_trie[sub_char]
                    if "whole_word" in curr_trie:
                        temp_word = curr_trie["whole_word"]
            if temp_word:
                word_exist_bool = True
                first_match_word = temp_word
            else:
                start_idx += 1
        return word_exist_bool, first_match_word

    def get_match_words(self, text: str, return_offset: bool = False) -> List:
        """vega FYI 从text的idx 0往后匹配,如果没有匹配到，
            接着从1开始匹配，如果匹配到了，
            假设长度为3，继续从索引3开始匹配
        """
        # TODO 返回匹配到的索引
        match_words_list = []
        text = text.lower() if self.stop_word else text
        text_len = len(text)
        start_idx = 0
        while start_idx <= text_len - 1:
            sub_text = text[start_idx:]
            temp_word, curr_trie = "", self.trie
            for sub_char in sub_text:
                if sub_char not in self.ignored_chars:
                    if sub_char not in curr_trie:
                        break
                    curr_trie = curr_trie[sub_char]
                    if "whole_word" in curr_trie:
                        temp_word = curr_trie["whole_word"]
            if temp_word:
                match_words_list.append(temp_word)
                start_idx += len(temp_word)
            else:
                start_idx += 1
        return match_words_list
