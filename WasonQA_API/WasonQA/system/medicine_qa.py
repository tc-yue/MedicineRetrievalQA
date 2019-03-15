# -*-coding:utf-8 -*-
from question_type_analysis.question_pattern import QuestionPattern
from question_type_analysis.pattern_match_strategy import PatternMatchStrategy
from question_type_analysis.pattern_match_result_selector import PatternMatchResultSelector
from question_type_analysis.pattern_based_question_classifier import PatternBasedMultiLevelQuestionClassifier
from evidence_retrieval.whoosh_data_source import WhooshDataSource
from evidence_retrieval.sql_data_source import SqlDataSource
from evidence_retrieval.baike_data_source import BaikeDataSource
from evidence_retrieval.solr_data_source import SolrDataSource
from score.evidence_score import EvidenceScore
from model.questiontype import QuestionType
from model.question import Question
from filter import evidence_filter
import logging
import re
import mqa_config
logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='mqa_config.QA_LOG_PATH',
                    filemode='w')


class MedicineQA:
    logging.info('开始构造Medicine问答系统')

    def __init__(self):
        # todo 数据库，文件等存到内存中
        pattern_match_strategy = PatternMatchStrategy()
        pattern_match_strategy.add_question_pattern(QuestionPattern.Question)
        pattern_match_strategy.add_question_pattern(QuestionPattern.TermWithNatures)
        pattern_match_strategy.add_question_pattern(QuestionPattern.Natures)
        # pattern_match_strategy.add_question_pattern(QuestionPattern.MainPartPattern)
        # pattern_match_strategy.add_question_pattern(QuestionPattern.MainPartNaturePattern)
        pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel1_true.txt')
        pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel2_true.txt')
        pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel3_true.txt')
        pattern_match_result_selector = PatternMatchResultSelector()
        self.__question_classifier = PatternBasedMultiLevelQuestionClassifier(pattern_match_strategy,
                                                                              pattern_match_result_selector)
        self.__evidence_score = EvidenceScore(mqa_config.SS_WEIGHTS)
        self.bds = BaikeDataSource()

    # 回答问题
    def answer_question(self, question_str):
        question = Question()
        question.set_question(question_str)
        question = self.__question_classifier.classify(question)
        logging.info('开始处理Question:'+question.question_string+question.question_type.value)
        logging.info(question.body+question.medicine+question.disease)
        if question.question_type == QuestionType.Medicine:
            answer = self.kb_based_answer_question(question)
            if not answer:
                answer = self.ir_based_answer_question(question)
        elif question.question_type == QuestionType.Definition \
                and len(question.body+question.medicine+question.disease) == 1:
            answer = self.baike_based_answer_question((question.body+question.medicine+question.disease)[0])
            if not answer:
                answer = self.ir_based_answer_question(question)
        else:
            answer = self.ir_based_answer_question(question)
        del question
        logging.info('候选答案: '+answer)
        return answer

    @staticmethod
    # todo 回带检索验证，证据评分
    def kb_based_answer_question(question):
        return SqlDataSource.select_medicine(question)

    def baike_based_answer_question(self, entity):
        return self.bds.search_defination(entity)

    def ir_based_answer_question(self, question):
        # if len(question.question_string) > 30 and len(question.main_part) > 0:
        #     evidences = WhooshDataSource.get_evidence(question.main_part)
        # else:
        #     evidences = WhooshDataSource.get_evidence(question.question_string)
        # evidences = SolrDataSource.get_evidence(question.word_list, question.medicine+question.disease+question.body)
        evidences = SolrDataSource.get_evidence(question.word_pos_list)
        question.add_evidences(evidences)
        if len(question.get_evidences()) == 0:
            logging.debug('无evidence')
            return '检索无答案'
        for i, evidence in enumerate(question.get_evidences()):
            logging.debug('开始处理第{}个Evidence：{}'.format(i, evidence.question_string))
            # 过滤
            # if evidence_filter.overfilter(question,evidence):
            #     continue
            self.__evidence_score.score(question, evidence)
        # 候选证据排序，获得评分第一的设定为期待答案
        evidences = sorted(question.get_evidences(), key=lambda ans: ans.get_score(), reverse=True)
        question.set_expect_answer(evidences[0].get_snippet())
        return question.get_expect_answer()
