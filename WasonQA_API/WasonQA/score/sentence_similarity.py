"""
问句相似度算法，包含各个打分模块
"""
from model.questiontype import QuestionType
from score.word_similarity import WordSimilarity
import logging
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib
from model.question import Question
import mqa_config

logging.info('加载词向量及字符级tfidf')
w2v = Word2Vec.load(mqa_config.WORD_VECTOR_PATH)
tfidf_model = joblib.load(mqa_config.CHAR_TFID_PATH)
logging.info('加载完毕')


def class_sim(question_type1, question_type2):
    """
    问句类型相似度
    :param question_type1: 问句类型
    """
    if question_type1 == question_type2:
        score = 1
    elif question_type1 is QuestionType.Solution or question_type2 is QuestionType.Solution:
        score = 0.5
    else:
        score = 0
    logging.info('类型\t得分为：{}'.format(score))
    return score


def word_sim(question1, question2):
    """
    词形相似度，用两个问句中含有共同词的个数来衡量，
    如果出现次数不同以出现少的数目为准
    :param question1: 句子分词后list
    """
    intersection_words = [w for w in question1 if w in question2]
    same_count = 0
    for i in intersection_words:
        a = question1.count(i)
        b = question2.count(i)
        if a >= b:
            same_count += b
        else:
            same_count += a
    score = 2*same_count/(len(question1)+len(question2))
    logging.info('词形\t得分为：{}'.format(score))
    return score


def order_sim(question1, question2):
    """
    词序相似度，用两个问句中词语的位置关系的相似程度
    :param question1: 问题的分词list
    """
    intersection_words = [w for w in question1 if w in question2
                          and question1.count(w) == 1 and question2.count(w) == 1]
    if len(intersection_words) <= 1:
        score = 0
    else:
        pfirst = sorted([question1.index(i) for i in intersection_words])
        psecond = [question2.index(question1[i]) for i in pfirst]
        count = 0
        for i in range(len(psecond)-1):
            if psecond[i] < psecond[i+1]:
                count += 1
        score = 1 - count/(len(intersection_words)-1)
    logging.info('词序\t得分为：{}'.format(score))
    return score


def wmd_sim(question1, question2):
    """
    :param question1: 问题的分词list
    """
    score = 1/(w2v.wmdistance(question1, question2)+1.0)
    logging.info('wmd\t得分：{}'.format(score))
    return score


def char_tfidf_sim(question1, question2):
    """
    字符级tfidf余弦相似度
    :param question_a：问题
    """
    score = float(cosine_similarity
                  (tfidf_model.transform([question1])[0],
                   tfidf_model.transform([question2])[0]))
    logging.info('字符级tfidf\t得分为：{}'.format(score))
    return score


def semantic_sim(question1, question2):
    """
    语义方法
    question1中每个词与2中每个词最相似
    :param question1: 问题list
    """
    word_similar = WordSimilarity()
    n = len(question1)
    score = 0.0
    for i in question1:
        word_sim_list = []
        # 平均时间3s
        for j in question2:
            word_sim_list.append(word_similar.get_similarity(i, j))
        score += max(word_sim_list)
    # score2 = 0.0
    # for j in range(m):
    #     score2 += max(self.word_similar.get_similarity(question1[i], question2[j]) for i in range(n))
    # score2 /= (2*n)
    word_similar.close_db()
    logging.info('语义\t得分：{}'.format(score))
    return score


def key_sim(question_a, question_b):
    """
    关键词相似度 包括疾病，疑问词，药品，身体部位，限制词
    :param question_a: 问题类
    """
    a = question_a.question_string
    b = question_b.question_string
    disease_cnt = 2 * len([i for i in question_a.disease if i in b])
    disease_less = len([i for i in question_a.disease if i not in b])
    question_cnt = 0.1 * len([i for i in question_a.question_words if i in b])
    medicine_cnt = len([i for i in question_a.medicine if i in b])
    body_cnt = 2 * len([i for i in question_a.body if i in b])
    body_less = len([i for i in question_a.body if i not in b])
    limits_cnt = len([i for i in question_a.limit if i in b])
    body_over = len([i for i in question_b.body if i not in a])
    disease_over = len([i for i in question_b.disease if i not in a])
    limits_over = len([i for i in question_b.limit if i not in a])
    score = disease_cnt + question_cnt + medicine_cnt + body_cnt + limits_cnt - limits_over * 5 - body_over \
            - disease_over - 3 * body_less - 3 * disease_less
    logging.info('关键词\t得分为：{}'.format(score))
    return score


def combination_sim(weights, question_a, question_b):
    """
    :param weights: dict 类型，各个评分组件的权重
    :param question_a: 问题类
    """
    logging.info('问句相似度开始')
    question1 = question_a.word_list
    question2 = question_b.word_list
    class_score = class_sim(question_a.question_type, question_b.question_type)
    key_score = key_sim(question_a, question_b)
    wmd_score = wmd_sim(question1, question2)
    # semantic_score = semantic_sim(question1, question2)
    word_score = word_sim(question1, question2)
    order_score = order_sim(question1, question2)
    char_tfidf_score = char_tfidf_sim(question_a.question_string, question_b.question_string)
    score = weights['class_weight']*class_score + weights['key_weight']*key_score + weights['wmd_weight']*wmd_score + \
            weights['word_weight']*word_score + weights['order_weight']*order_score + \
            weights['char_tfidf_weight']*char_tfidf_score
    logging.info('问句相似度结束,得分为{}\n\n'.format(score))
    return score


if __name__ == '__main__':
    q = Question()
    q.set_question('感冒了怎么办')
    que = input()
    while que != 'end':
        q2 = Question()
        q2.set_question(que)
    # q.set_question_type(QuestionType.Doctor)
        combination_sim()
        que = input()
