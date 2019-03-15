import sys
from word_parser import parser
from model.questiontype import QuestionType


class Question:
    def __init__(self):
        """
        依次为  问题字符串，带词性分词，去停用词分词，问题类型，候选问题类型，证据列表，候选答案
        问题疾病，药物，身体，疑问词
        """
        self.__question_string = ''
        self.__word_pos_list = []
        self.__word_list = []
        self.__question_type = QuestionType.Solution
        self.__candidate_question_types = set()
        self.__evidences = []
        self.__expect_answer = ''
        self.__disease = []
        self.__medicine = []
        self.__body = []
        self.__question_key_words = []
        self.__limit = []
        self.__main_part = ''

    def set_question(self, question):
        self.__question_string = question
        self.__word_pos_list = parser.parse(self.__question_string)
        self.__word_list = parser.lcut(self.__question_string)
        self.__disease, self.__medicine, self.__body, self.__question_key_words, self.__limit, self.__main_part \
            = parser.medicine_rule_based_ner(self.__word_pos_list)

    @property
    def question_string(self):
        return self.__question_string

    @property
    def word_list(self):
        return self.__word_list

    @property
    def word_pos_list(self):
        return self.__word_pos_list

    @property
    def disease(self):
        return self.__disease

    @property
    def main_part(self):
        return self.__main_part

    @property
    def question_words(self):
        return self.__question_key_words

    @property
    def medicine(self):
        return self.__medicine

    @property
    def body(self):
        return self.__body

    @property
    def limit(self):
        return self.__limit

    @property
    def question_type(self):
        return self.__question_type

    @question_type.setter
    def question_type(self, question_type):
        self.__question_type = question_type

    def get_text(self):
        text = ''
        for evidence in self.__evidences:
            text += evidence.get_title() + evidence.get_snippet()
        return text

    def get_evidences(self):
        return self.__evidences

    def add_evidences(self, evidences):
        self.__evidences.extend(evidences)

    def add_evidence(self, evidence):
        self.__evidences.append(evidence)

    def remove_evidence(self, evidence):
        self.__evidences.remove(evidence)

    def get_expect_answer(self):
        return self.__expect_answer

    def set_expect_answer(self, expect_answer):
        self.__expect_answer = expect_answer


if __name__ == '__main__':
    q = Question()
    q.set_question('宝宝肛门红肿怎么办')
