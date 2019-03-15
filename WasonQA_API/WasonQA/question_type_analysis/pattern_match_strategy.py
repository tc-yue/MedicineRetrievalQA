from question_type_analysis import question_pattern

"""
问题匹配策略
问题类型模式文件
问题模式
"""


class PatternMatchStrategy:
    def __init__(self):
        self.__question_type_pattern_files = []
        self.__question_patterns = []

    def add_question_type_pattern_files(self, question_type_file):
        self.__question_type_pattern_files.append(question_type_file)

    def add_question_pattern(self, question_pattern1):
        self.__question_patterns.append(question_pattern1)

    def enable_question_type_pattern_file(self, question_type_pattern_file):
        if question_type_pattern_file in self.__question_type_pattern_files:
            return True
        else:
            return False

    def enable_question_pattern(self, question_pattern1):
        if question_pattern1 in self.__question_patterns:
            return True
        else:
            return False

    def get_strategy_des(self):
        string = ''
        for question_type_pattern_file in self.__question_type_pattern_files:
            string = string+question_type_pattern_file+':'
        for question_pattern1 in self.__question_patterns:
            string = string+str(question_pattern1)+':'
        return string
