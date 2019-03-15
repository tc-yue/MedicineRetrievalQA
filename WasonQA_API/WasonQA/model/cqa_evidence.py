import sys
sys.path.append('../')
from word_parser import parser
from model.question import Question


"""
Cqa证据继承Question类
由原始问题 和snippet：回答 组成 

"""


class CqaEvidence(Question):

    def __init__(self):
        # 元素类型CandidateAnswer的实例
        super(CqaEvidence, self).__init__()
        self.__score = 0.0
        self.__snippet = ''
        self.__snippet_words = []

    def set_snippet(self, snippet):
        self.__snippet = snippet

    def get_snippet(self):
        return self.__snippet

    def get_snippet_words(self):
        self.__snippet_words = parser.lcut(self.__snippet)
        return self.__snippet_words

    def get_score(self):
        return self.__score

    def add_score(self, score):
        self.__score += score


if __name__ == '__main__':
    q = CqaEvidence()
    q.set_question('宝宝肛门红肿怎么办')
    print(q.question_string)

