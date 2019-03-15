# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 21:04
# @Author  : Tianchiyue
# @File    : question_classification.py
# @Software: PyCharm Community Edition

import re
import mqa_config


with open(mqa_config.JIEBA_POS_PATH, 'r', encoding='utf-8')as f:
    medicine_clf_key = f.readlines()[184:]


def medicine_clf(sentence):
    """
    根据是否包含医药相关词分类
    """
    medicine_clf_pattern = '|'.join([i.split(' ')[0] for i in medicine_clf_key if '(' not in i and '-' not in i])
    return re.search(medicine_clf_pattern, sentence)