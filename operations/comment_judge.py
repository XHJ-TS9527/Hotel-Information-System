#导入包
import pickle
import jieba
import jieba.posseg as pseg
import re
from gensim.models import Word2Vec
import numpy as np
jieba.setLogLevel(20)

class comment_judger():
    def __init__(self):
        self.punctuation='！，。；：.,“”（）'
        self.allow_word=('a','an','b','ad','d','v','l')
        self.model=Word2Vec.load(r'../operations/model/ftext0.model')
        self.label={0:'消极',1:'积极'}
        self.ref_word=('坏','差','吵','脏','好','满意','不错','新')
        self.model_dir=r'../operations/model/svm.pkl'
        with open(self.model_dir,'rb') as f:
            self.svm=pickle.load(f)
    
    def remove_punctuation(self,text):
        text=re.sub(r'[{}]+'.format(self.punctuation),'',text)
        return text.strip().lower()
    
    def make_vec(self,content):
        cnt=0
        each_sentence=[]
        for cont in content:
            ref=[]
            for each_word in self.ref_word:
                ref.append(self.model.similarity(cont,each_word))
            ref=np.array(ref).reshape([1,-1])
            if not cnt:
                each_sentence=ref
                cnt+=1
            else:
                each_sentence=np.concatenate((each_sentence,ref))
        each_sentence=np.mean(each_sentence,axis=0)
        return each_sentence
    
    def comment_judge(self,comment_text):
        sentence=comment_text.strip('\n')
        sentence=self.remove_punctuation(sentence)
        content=[]
        for each in pseg.lcut(sentence):
            if each.flag in self.allow_word:
                content.append(each.word)
        vec=self.make_vec(content).reshape([1,-1])
        return self.label[int(self.svm.predict(vec))]