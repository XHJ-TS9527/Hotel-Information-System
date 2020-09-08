import pickle
import jieba.posseg as pseg
import re
from gensim.models import Word2Vec
import numpy as np

punctuation = '！，。；：.,“”（）'
allow_word = ['a', 'an','b', 'ad', 'd', 'v', 'l']
model = Word2Vec.load(r'./model/ftext0.model')
label = {0: 'neg', 1: 'pos'}
ref_word = ['坏', '差', '吵', '脏', '好', '满意', '不错', '新']

model_dir = r'./model/svm.pkl'

with open(model_dir, 'rb') as f:
    svm = pickle.load(f)

def removePunctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip().lower()

def split_sen(file):
    with open(file, 'r', encoding='utf-8') as f:
        con = []
        line = f.readlines()
        for each in line:
            each = each.strip('\n')
            each = removePunctuation(each)
            if '' == each:
                continue
            each = pseg.lcut(each)
            con1 = []
            for each1 in each:
                if each1.flag in allow_word:
                    con1.append(each1.word)

            con.extend(con1)
    return con

def mk_vec(sen):
    cnt1 = 0
    each_sen = []
    for i1 in sen:
        each_ref = []
        for each in ref_word:
            r0 = model.similarity(i1, each)
            each_ref.append(r0)

        each_ref = np.array(each_ref)
        each_ref = each_ref.reshape([1,-1])
        if cnt1 == 0:
            each_sen = each_ref
            cnt1 += 1
        else:
            each_sen = np.concatenate((each_sen, each_ref))

    each_sen = np.mean(each_sen, axis=0)

    return each_sen

def predict_txt(txt_dir):

    content = split_sen(txt_dir)
    vec = mk_vec(content)
    vec = vec.reshape([1, -1])
    class0 = svm.predict(vec)

    return label[int(class0)]

def predict_sen(sentence):
    sen = sentence.strip('\n')
    sen = removePunctuation(sen)
    con = []
    sen0 = pseg.lcut(sen)
    for each1 in sen0:
        if each1.flag in allow_word:
            con.append(each1.word)

    vec = mk_vec(con)
    vec = vec.reshape([1,-1])
    class0 = svm.predict(vec)

    return label[int(class0)]







