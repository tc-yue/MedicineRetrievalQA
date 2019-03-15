# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 22:01
# @Author  : Tianchiyue
# @File    : conversation_manager.py.py
# @Software: PyCharm Community Edition

import requests
import logging
from question_type_analysis import question_classification
from system.medicine_qa import MedicineQA
import mqa_config
import time
import datetime

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename=mqa_config.QA_LOG_PATH,
                    filemode='w')


def tl_chat(question_str, tuling_key,tuling_user_id, tuling_url):
    args = {'key': tuling_key, 'info': question_str, 'userid': str(tuling_user_id)}
    response = requests.post(url=tuling_url, data=args)
    res_json = response.json()
    if 'text' not in res_json:
        raise Exception(str(res_json))
    return res_json['text']


class QuestionAnsweringSystem:
    logging.info('开始构造对话系统')

    def __init__(self):
        self.medicine_qa = MedicineQA()
        self.tuling_key, self.tuling_url = mqa_config.TULING_API.values()

    # 回答问题
    def answer_question(self, question_str, user_id):
        """
        调用分类器，根据分类结果调用不同的QA系统
        :param user_id:用于维护图灵api的用户id
        :return:
        """
        if not question_classification.medicine_clf(question_str):
            return tl_chat(question_str, self.tuling_key, user_id, self.tuling_url)
        return self.medicine_qa.answer_question(question_str)

