# -*- coding: utf-8 -*-
# @Time    : 2018/1/12 11:24
# @Author  : Tianchiyue
# @File    : mqa_config.py.py
# @Software: PyCharm Community Edition
import os

PATH = os.path.abspath(os.path.dirname(__file__) + os.path.sep)
WORD_VECTOR_PATH = os.path.join(PATH + '/files/medicine.model')
CHAR_TFID_PATH = os.path.join(PATH + '/files/char_tfidf.m')
INDEX_PATH = os.path.join(PATH + '/files/indexer')
QA_DB_PATH = os.path.join(PATH + '/files/qapairs.db')
MEDICINE_DB_PATH = os.path.join(PATH + '/files/medicine.db')
STOPS_PATH = os.path.join(PATH + '/files/dic/stops.txt')
JIEBA_POS_PATH = os.path.join(PATH + '/files/dic/jieba_pos.txt')
STOPS_PKL_PATH = os.path.join(PATH + '/files/dic/stops.pkl')
QA_LOG_PATH = os.path.join(PATH + '/qa.log')
QUESTION_TYPE_PATTERN_PATH = os.path.join(PATH+'/files/questionTypePattern/')
SOLR_GET_URL = 'http://202.118.75.247:8983/solr/medicineqa/select?'

MYSQL = {'host': '202.118.75.247',  # 默认127.0.0.1
         'user': 'xty',
         'password': 'dlut2018',
         'port': 13306,  # 默认即为3306
         'database': 'xtydb',
         'charset': 'utf8'  # 默认即为utf8
         }

SS_WEIGHTS = {'order_weight': 0.1,
              'word_weight': 0.7,
              'class_weight': 0.1,
              'key_weight': 1.0,
              'wmd_weight': 1.9,
              'syntax_weight': 0.1,
              'semantic_weight': 0.3,
              'char_tfidf_weight': 0.9
              }

TULING_API = {'key': '2c5feeb4bb3248e7957972b37cb24f95',
              'url': 'http://www.tuling123.com/openapi/api'
              }

SPIDER_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                  'Connection': 'keep-alive',
                  'Host': 'baike.baidu.com',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}