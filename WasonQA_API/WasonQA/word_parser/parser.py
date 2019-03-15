import jieba
import jieba.posseg
import pickle
import mqa_config

jieba.load_userdict(mqa_config.JIEBA_POS_PATH)
# TODO 停用词表细化
with open(mqa_config.STOPS_PATH, 'r',encoding='utf8',errors='ignore')as f:
    stop_list = f.read().split('\n')


def parse(sentence):
    """
    去停用词的词性识别
    :param sentence:句子字符串
    :return: 包含分词和词性标注tuple 的list
    """
    return [(word, flag) for word, flag in jieba.posseg.cut(sentence) if word not in stop_list]


def lcut(sentence):
    """
    去停用词分词
    """
    return [word for word in jieba.cut(sentence) if word not in stop_list]


def medicine_rule_based_ner(word_pos_list):
    """
    MedicineQA基于jieba分词的词性识别来抽取实体。
    :param word_pos_list: jieba分词的词性
    """
    # TODO 实体抽取还需要更准
    disease = [i[0] for i in word_pos_list if i[1] == 'nobjectdisease']
    medicine = [i[0] for i in word_pos_list if i[1] == 'nmedicinename']
    body = [i[0] for i in word_pos_list if i[1] == 'nobjectbodypart']
    question_key_words = [i[0] for i in word_pos_list if i[1].startswith('rw')]
    limit = [i[0] for i in word_pos_list if i[1] == 'nlimit']
    noun = ''.join([i[0] for i in word_pos_list if i[1].startswith('n')])
    return disease, medicine, body, question_key_words, limit, noun
