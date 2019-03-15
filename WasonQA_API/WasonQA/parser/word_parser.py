import jieba
import jieba.posseg
import pickle
import os

path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)
jieba.load_userdict(path+'/files/dic/jieba_pos.txt')
# TODO 停用词表细化
with open(path+'/files/dic/stops.pkl', 'rb')as f:
    stop_list = pickle.load(f)


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
    medicine = [i[0] for i in word_pos_list if i[1] == 'nobjectmedicine']
    body = [i[0] for i in word_pos_list if i[1] == 'nobjectbodypart']
    question_key_words = [i[0] for i in word_pos_list if i[1].startswith('rw')]
    limit = [i[0] for i in word_pos_list if i[1] == 'nlimit']
    noun = ''.join([i[0] for i in word_pos_list if i[1].startswith('n')])
    return disease, medicine, body, question_key_words, limit, noun


if __name__ == '__main__':
    que =['牙受伤了怎么办',
          '焦虑怎么办',
          '肠胃特别好怎么办',
          '鼻子流血',
          '牙龈红肿怎么办',
          '左下腹疼痛是因为什么',
          '眼睛疼怎么办',
          '熬夜了，眼睛感觉很头疼怎么办',
          '妇科病怎么治',
          '感康的成分是什么']
    for j in que:
        wpl = parse(j)
        print(medicine_rule_based_ner(wpl))
