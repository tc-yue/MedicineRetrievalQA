# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 19:40
# @Author  : Tianchiyue
# @File    : sql_data_source.py
# @Software: PyCharm Community Edition
import sqlite3
import logging
from collections import Counter
import mqa_config
import os

class SqlDataSource(object):

    @staticmethod
    def select_medicine(question):
        """
        通过疾病，搜索对应药名
        """
        logging.info('数据库查询开始')
        conn = sqlite3.connect(mqa_config.MEDICINE_DB_PATH)
        cursor = conn.cursor()
        medicine_list = []
        disease_list = question.disease
        for i in disease_list:
            cursor.execute("select NAME from MEDICINE where INDICATIONS like ?", ['%'+i+'%'])
            values = cursor.fetchall()
            medicine_list += [item[0] for item in values]
        top_list = Counter(medicine_list).most_common(3)
        cursor.close()
        conn.commit()
        conn.close()
        logging.info('数据库查询结束')
        return [i[0] for i in top_list]