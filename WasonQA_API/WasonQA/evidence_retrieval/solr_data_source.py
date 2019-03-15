# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 9:58
# @Author  : Tianchiyue
# @File    : solr_data_source.py
# @Software: PyCharm Community Edition
import requests
import mqa_config
import logging
from model.cqa_evidence import CqaEvidence


class SolrDataSource:

    @staticmethod
    def get_evidence(pos_list):
        logging.info('获取支持证据开始')
        # 可以加AND模式
        # query = 'answer_cut:牙疼;肚子;感冒 AND answer_cut:感冒 AND answer_cut:发烧'
        # and_added = ' '.join(['AND question_cut:{}'.format(word) for word in key_words[:3]])
        question_words = [i+'^'+str(3) if j in ['nmedicinename','nobjectdisease','nobjectbodypart'] else i for i, j in pos_list]
        query = 'question_cut:{}'.format(';'.join(question_words))
        query_params = {'q': query,
                        'fl': 'question,answer',
                        'wt': 'json',
                        'rows': 20,
                        #                 ,'q.op':'OR'
                        }
        response_json = requests.get(mqa_config.SOLR_GET_URL, params=query_params).json()
        evidences = []
        for item in response_json['response']['docs']:
            evidence = CqaEvidence()
            evidence.set_question(item['question'][0])
            evidence.set_snippet(item['answer'][0])
            evidences.append(evidence)
        logging.info('获取支持证据结束')
        return evidences
