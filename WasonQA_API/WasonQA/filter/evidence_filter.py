# -*- coding: utf-8 -*-
# @Time    : 2018/1/12 17:17
# @Author  : Tianchiyue
# @File    : evidence_filter.py
# @Software: PyCharm Community Edition


def over_filter(question_a, question_b):
    body_over = len([i for i in question_b.body if i not in question_a.question_string])
    disease_over = len([i for i in question_b.disease if i not in question_a.question_string])
    limits_over = len([i for i in question_b.limit if i not in question_a.question_string])
    if (body_over+disease_over+limits_over) > 5:
        return False
    else:
        return True