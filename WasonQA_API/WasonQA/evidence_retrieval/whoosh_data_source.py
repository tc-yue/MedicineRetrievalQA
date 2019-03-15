import sqlite3
import logging
from whoosh.index import open_dir
from whoosh.qparser import OrGroup, QueryParser
from model.cqa_evidence import CqaEvidence
from model.question import Question
import mqa_config
import mysql.connector


class WhooshDataSource:

    @staticmethod
    def index_open(word):
        results_list = []
        ix = open_dir(mqa_config.INDEX_PATH)
        conn = sqlite3.connect(mqa_config.QA_DB_PATH)
        cursor1 = conn.cursor()
        qp = QueryParser("title", schema=ix.schema, group=OrGroup)
        parser = qp.parse(word)
        logging.info(parser)
        with ix.searcher() as search:
            results = search.search(parser, limit=20)
            id_list = [int(result['id']) for result in results[:20]]
            for i in id_list:
                try:
                    cursor1.execute("select * from QAPAIRS WHERE ID = ?", (i,))
                    values = cursor1.fetchall()[0]
                except Exception as e:
                    logging.error(e)
                else:
                    results_list.append((values[1], values[2]))
        cursor1.close()
        conn.commit()
        conn.close()
        return results_list

    @staticmethod
    def index_open_mysql(cursor, word):
        ix = open_dir(mqa_config.INDEX_PATH)
        qp = QueryParser("title", schema=ix.schema, group=OrGroup)
        parser = qp.parse(word)
        logging.info(parser)
        with ix.searcher() as search:
            results = search.search(parser, limit=20)
            id_tuple = [int(result['id']) for result in results[:20]]
            cursor.execute("select * from qapairs WHERE ID IN " + str(tuple(id_tuple)))
            values = cursor.fetchall()
        return [(value[1], value[2]) for value in values]

    @staticmethod
    def get_evidence(question_str):
        logging.info('获取支持证据开始')
        evidences = []
        elements = WhooshDataSource.index_open(question_str)
        for item in elements:
            evidence = CqaEvidence()
            evidence.set_question(item[0])
            evidence.set_snippet(item[1])
            evidences.append(evidence)
        logging.info('获取支持证据结束')
        return evidences


if __name__ == '__main__':
    a = Question()
    que_list = ['我今天吃了一个麻辣烫，很辣很热，到了晚上肚子疼，闹肚子，想吐，要怎么办',
                # '牙疼，牙龈红肿肿胀，口角气泡，牙龈经常出血怎么办',
                # '感冒，发烧流鼻涕，昨天还咳嗽，天气太冷了，怎么办',
                # '昨天吃西瓜，今天拉肚子了，不停怎么办，有什么方法',
                '昨天骑车摔倒了，腿磕破了，有点出血很痛']
    conn = mysql.connector.connect(**mqa_config.MYSQL)
    cursor = conn.cursor()
    for i in que_list:
        b = WhooshDataSource.index_open(i)
        print(b)
        c = WhooshDataSource.index_open_mysql(cursor,i)
        print(c)
