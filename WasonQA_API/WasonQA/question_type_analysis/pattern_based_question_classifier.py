import os
import re
import logging
from model.question import Question
from word_parser import parser
from question_type_analysis.question_pattern import QuestionPattern
from question_type_analysis.pattern_match_result import PatternMatchResult
from question_type_analysis.pattern_match_strategy import PatternMatchStrategy
from question_type_analysis.pattern_match_result_item import PatternMatchResultItem
from question_type_analysis.question_type_pattern_file import QuestionTypePatternFile
from question_type_analysis.pattern_match_result_selector import PatternMatchResultSelector
from question_type_analysis.question_type_transformer import QuestionTypeTransformer
import mqa_config
logging.basicConfig(level=logging.CRITICAL,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        filename=mqa_config.QA_LOG_PATH,
                        filemode='w')

"""
模式匹配判断类型
5种方式 和问题，词和词性，词性，主干词和词性，主干词性 匹配
"""


class PatternBasedMultiLevelQuestionClassifier:

    def __init__(self, pattern_match_strategy1, pattern_match_result_selector1):
        self.__question_pattern_cache = {}
        self.__question_type_pattern_cache = {}
        self.__question_type_pattern_files = []
        self.__pattern_match_strategy = pattern_match_strategy1
        self.__pattern_match_result_selector = pattern_match_result_selector1
        for item in sorted(os.listdir(mqa_config.QUESTION_TYPE_PATTERN_PATH)):
            logging.info('\t模式文件'+item)
            attr = item.split('_')
            file = QuestionTypePatternFile()
            file.set_file(item)
            if 'true' in attr[1]:
                multi_match = True
            else:
                multi_match = False
            file.set_multi_match(multi_match)
            self.__question_type_pattern_files.append(file)

    def classify(self, q):
        question_str = q.question_string
        pattern_match_strategy1 = self.get_pattern_match_strategy()
        question_patterns = self.extract_pattern_from_question(question_str, pattern_match_strategy1)
        if len(question_patterns) == 0:
            logging.error('提取问题模式失败')
            return q
        pattern_match_result = PatternMatchResult()
        for qtpfile in self.__question_type_pattern_files:
            question_type_pattern_file1 = qtpfile.get_file()
            logging.info('处理问题类型模式文件： '+qtpfile.get_file())
            question_type_pattern1 = self.extract_question_type_pattern(question_type_pattern_file1)
            if question_type_pattern1 is not None:
                pattern_match_result_items = self.get_pattern_match_result_items(question_patterns, question_type_pattern1)
                if len(pattern_match_result_items) == 0:
                    logging.info('在问题类型模式中未找到匹配项: '+question_type_pattern_file1)
                else:
                    pattern_match_result.add_pattern_match_result(qtpfile,pattern_match_result_items)
                    logging.info('在问题类型模式中找到匹配项: '+question_type_pattern_file1)
            else:
                logging.info('处理问题类型模式文件失败: '+question_type_pattern_file1)
        pattern_match_result_items = pattern_match_result.get_all_pattern_match_result()
        if len(pattern_match_result_items) == 0:
            logging.info('问题没有匹配到任何模式')
            return q
        if len(pattern_match_result_items) > 1:
            logging.info('问题匹配到多个模式')
            i = 1
            for item in pattern_match_result_items:
                logging.info('序号: '+str(i))
                logging.info('\t问题: '+item.get_origin())
                logging.info('\t模式: ' + item.get_pattern())
                logging.info('\t分类: '+item.get_type())
                i += 1
        # for file in pattern_match_result.get_questiontypepatternfiles_compacttoloose():
        #     logging.info(file.get_file()+'是否允许多匹配')
        #     i = 1
        #     for item in pattern_match_result.get_pattern_match_result(file):
        #         logging.info('序号'+str(i))
        #         logging.info('\t问题'+item.get_origin())
        #         logging.info('\t模式' + item.get_pattern())
        #         logging.info('\t分类'+item.get_type())
        #         i += 1
        q.question_type = QuestionTypeTransformer.transform(pattern_match_result.get_max_result())
        return q
        # return PatternMatchResultSelector.select(q, pattern_match_result)

    def get_pattern_match_strategy(self):
        return self.__pattern_match_strategy

    def set_pattern_match_strategy(self, pattern_match_strategy1):
        self.__pattern_match_strategy = pattern_match_strategy1

    def get_pattern_match_result_selector(self):
        return self.__pattern_match_result_selector

    def set_pattern_match_result_selector(self, pattern_match_result_selector1):
        self.__pattern_match_result_selector = pattern_match_result_selector1

    def extract_pattern_from_question(self, question1, pattern_match_strategy1):
        """
        抽取问题模式
        :param question1:问题字符串
        :param pattern_match_strategy1:模式匹配策略
        """
        logging.info('开始抽取问题模式')
        question_patterns = []
        question1 = question1.strip()
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.Question):
            question_patterns.append(question1)
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.TermWithNatures) or \
                pattern_match_strategy1.enable_question_pattern(QuestionPattern.Natures):
            term_with_nature = self.__question_pattern_cache.get(question1 + 'term_with_natures')
            nature = self.__question_pattern_cache.get(question1 + 'nature')
            if term_with_nature is None or nature is None:
                words = parser.parse(question1)
                term_with_nature_str = ''
                nature_str = ''
                i = 0
                for word in words:
                    term_with_nature_str += word[0] + '/' + word[1] + ' '
                    if i > 0:
                        nature_str += '/'
                    i += 1
                    nature_str += word[1]
                # self.__question_pattern_cache[question1 + 'term_with_nature'] = term_with_nature_str
                # self.__question_pattern_cache[question1 + 'nature'] = nature_str
                if pattern_match_strategy1.enable_question_pattern(QuestionPattern.TermWithNatures):
                    question_patterns.append(term_with_nature_str)
                    logging.info('词和词性序列： '+term_with_nature_str)
                if pattern_match_strategy1.enable_question_pattern(QuestionPattern.Natures):
                    question_patterns.append(nature_str)
                    logging.info('词性序列： ' + nature_str)
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.MainPartNaturePattern) or \
                pattern_match_strategy1.enable_question_pattern(QuestionPattern.MainPartPattern):
            response = LtpDependencyParsing.get_dp_json(question1)
            try:
                dp_data = response.json()
                question1 = LtpDependencyParsing.get_main_part(dp_data)
                # mpnp = self.__question_pattern_cache.get(question1 + 'mainpnp')
                # mpp = self.__question_pattern_cache.get(question1 + 'mainpp')
                if mpnp is None or mpp is None:
                    words = parser.parse(question1)
                    mpp_str = ''
                    mpnp_str = ''
                    i = 0
                    for word in words:
                        mpp_str += word[0] + '/' + word[1] + ' '
                        if i > 0:
                            mpnp_str += '/'
                        i += 1
                        mpnp_str += word[1]
                    if pattern_match_strategy1.enable_question_pattern(QuestionPattern.MainPartNaturePattern):
                        self.__question_pattern_cache[question1 + 'mainpnp'] = mpnp_str
                        question_patterns.append(mpnp_str)
                        logging.info('主谓宾词性序列'+mpnp_str)
                    if pattern_match_strategy1.enable_question_pattern(QuestionPattern.MainPartPattern):
                        self.__question_pattern_cache[question1 + 'mainpp'] = mpp_str
                        question_patterns.append(mpp_str)
                        logging.info('主谓宾词和词性序列'+mpp_str)
            except Exception as e:
                logging.error('main_part failed')
                logging.error(e)
        return question_patterns

    # 从问题类型模板文件中提取
    def extract_question_type_pattern(self, question_type_pattern_file1):
        value = self.__question_type_pattern_cache.get(question_type_pattern_file1)
        # 将问题类型模式存储到cache中
        if value:
            return value
        types = []
        patterns = []
        with open(os.path.join(mqa_config.QUESTION_TYPE_PATTERN_PATH+question_type_pattern_file1), 'r', encoding='utf8') as f:
            lines = f.readlines()
            try:
                for line in lines:
                    types.append(line.split(' ')[0])
                    patterns.append(line.split(' ')[1].replace('\n', ''))
            except Exception as e:
                logging.error(e)
        question_type_pattern = QuestionTypePattern()
        question_type_pattern.set_patterns(patterns)
        question_type_pattern.set_types(types)
        self.__question_type_pattern_cache[question_type_pattern_file1] = question_type_pattern
        return question_type_pattern

    # 获取模式匹配项
    @staticmethod
    def get_pattern_match_result_items(question_patterns, question_type_pattern):
        if question_patterns is None or len(question_patterns) == 0:
            return None
        if question_type_pattern is None or len(question_type_pattern.get_patterns()) == 0:
            return None
        pattern_match_result_items = []
        patterns = question_type_pattern.get_patterns()
        types = question_type_pattern.get_types()
        p_length = len(patterns)
        for i in range(p_length):
            pattern = patterns[i]
            for question_pattern in question_patterns:
                m = re.match(pattern, question_pattern)
                if m:
                    item = PatternMatchResultItem()
                    item.set_origin(question_pattern)
                    item.set_pattern(pattern)
                    item.set_type(types[i])
                    pattern_match_result_items.append(item)
        return pattern_match_result_items

"""
问题类型模式
指定问题类型和问题模式的关系
如1、Person-> Multi2 ...
"""


class QuestionTypePattern:
    def __init__(self):
        # 所有问题类型
        self.types = []
        # 所有问题模式
        self.patterns = []

    def get_types(self):
        return self.types

    def set_types(self, types):
        self.types = types

    def get_patterns(self):
        return self.patterns

    def set_patterns(self, patterns):
        self.patterns = patterns
