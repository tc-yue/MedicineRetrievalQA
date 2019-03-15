# -*- coding: utf-8 -*-
# @Time    : 2018/1/13 20:10
# @Author  : Tianchiyue
# @File    : test.py
# @Software: PyCharm Community Edition
import sqlite3
import mysql.connector
import time
import mqa_config
import os
import logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        filename='E:\XiaoTaiYi\WasonQA_API\WasonQA\qa.log',
                        filemode='w')


def sqlite_time():
    conn_ite = sqlite3.connect(os.path.join(mqa_config.PATH, 'files/qapairs.db'))
    cursor_ite = conn_ite.cursor()
    start = time.clock()
    cursor_ite.execute('select * from qapairs where id < 10')
    end = time.clock()
    items = cursor_ite.fetchall()
    print(items)
    cursor_ite.close()
    conn_ite.close()
    print(end - start)


def mysql_time():
    config = mqa_config.MYSQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    start = time.clock()

    cursor.execute('select * from qapairs where id <10 ' )
    values = cursor.fetchall()
    print(values)
    end = time.clock()
    logging.info(end-start)
    cursor.close()
    # values = cursor.fetchall()
    # print(values)
    # conn.commit()
    conn.close()


if __name__ == '__main__':
    print(os.path.join(mqa_config.PATH, 'files/qapairs.db'))
    sqlite_time()
    mysql_time()
