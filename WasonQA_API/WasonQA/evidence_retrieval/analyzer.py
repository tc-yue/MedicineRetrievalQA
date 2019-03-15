from whoosh.analysis import StopFilter
from whoosh.analysis import Tokenizer, Token
import jieba
import re
import mqa_config
import os

"""
Whoosh 中文分词器
"""


with open(mqa_config.STOPS_PATH, 'r', encoding='gbk')as f:
    STOP_WORDS = set(f.read().split('\n'))

accepted_chars = re.compile(r"[\u4E00-\u9FD5]+")


class ChineseTokenizer(Tokenizer):

    def __call__(self, text, **kargs):
        # mode = search ? 查询速度较慢，生成索引时可以使用
        words = jieba.tokenize(text, 
                               #mode='search'
                               )
        token = Token()
        for (w, start_pos, stop_pos) in words:
            if not accepted_chars.match(w) and len(w) <= 1:
                continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token


def ChineseAnalyzer(stoplist=STOP_WORDS, minsize=1):
    return (ChineseTokenizer() | StopFilter(stoplist=stoplist, minsize=minsize))
