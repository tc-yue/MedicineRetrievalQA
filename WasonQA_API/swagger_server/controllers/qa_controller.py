import connexion
from swagger_server.models.answer import Answer
from swagger_server.models.question import Question
from datetime import date, datetime
from typing import List, Dict
from six import iteritems

from WasonQA.conversation_manager import QuestionAnsweringSystem
from ..util import deserialize_date, deserialize_datetime

wason_qa = QuestionAnsweringSystem()
print('wason api ready!')
def api_post(body):
    """
    QA
    Answer Questions, XiaoTaiYi 
    :param body: question object
    :type body: dict | bytes

    :rtype: Answer
    """

    if connexion.request.is_json:
        body = Question.from_dict(connexion.request.get_json())
        if body.key=='dut2018':
            print(body.userid,body.info)
            answer=wason_qa.answer_question(body.info,body.userid)
            result={'code':'100000','text':answer}
        else:
            result={'code':'0','text':'key error!'}
    else:
        result={'code':'0','text':'data error!'}
    return result
