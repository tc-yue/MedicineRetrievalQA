# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 15:28
# @Author  : Tianchiyue
# @File    : baike_data_source.py
# @Software: PyCharm Community Edition
import re
import requests
import mqa_config
import logging

spider_header = mqa_config.SPIDER_HEADERS


class BaikeDataSource(object):
    def __init__(self):
        self.entity_definition_cache = {}

    def search_defination(self, entity):
        """
        搜索实体的定义
        """
        logging.info('百科查询开始')
        if self.entity_definition_cache.get(entity):
            return self.entity_definition_cache[entity]
        try:
            res = requests.get('https://baike.baidu.com/item/' + entity, headers=spider_header)
            content = res.content.decode('utf8')
            reg_content = '<div class="lemma-summary" label-module="lemmaSummary">[\s\S]+?</div>'
            content = re.findall(reg_content, content)[0]
            content = re.sub('<.+?>|\n', '', content)
            logging.info('百科查询结束')
            self.entity_definition_cache[entity] = content
            return content
        except Exception as e:
            logging.WARNING(e)
            return False

