import xgboost as xgb
import json
import pickle
import pandas as pd
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import KeyedVectors

# from matplotlib import pyplot as plt
# import collections
# from sklearn import cross_validation
def cnt_days(text):
    if pd.isna(text) or text == '':
        return np.nan
    else:
        text_y = ''
        text_m = ''
        if 'и' in text:
            text_y = text[:text.index('и')]
            text_m = text[text.index('и') + 1:]
        elif ('год' in text) or ('лет' in text):
            text_y = text
        elif ('месяц' in text):
            text_m = text

        num_y = 0
        num_m = 0
        if text_y != '':
            num_y = int("".join(filter(str.isdigit, text_y)))
        if text_m != '':
            num_m = int("".join(filter(str.isdigit, text_m)))
        print('count_days')
        return (num_y * 360 + num_m * 30)


def dist_betw_sent(sent1, sent2, model):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!', type(sent1), type(sent2))
    if pd.isna(sent1) or pd.isna(sent2) or sent1 == '' or sent2 == '':
        return np.nan
    else:
        print('aaaaaaaaaaa')
        words1 = re.sub(r'[^\w\s]', '', str(sent1)).split()
        print(words1,'words1')
        words2 = re.sub(r'[^\w\s]', '', str(sent2)).split()
        print(words2, 'words2')
        vec1 = np.zeros(300)
        for word in words1:
            if (word.lower() + '_NOUN') in model:
                print('yes1')
                vec1 += model[word.lower() + '_NOUN']
                print(sum(vec1),'sum')
        vec2 = np.zeros(300)
        for word in words2:
            if (word.lower() + '_NOUN') in model:
                vec2 += model[word.lower() + '_NOUN']
        # for word in words1:
        #     try:
        #         vec1 += model[word + '_NOUN']
        #     except:
        #         pass
        # vec2 = np.zeros(300)
        # for word in words2:
        #     try:
        #         vec2 += model[word + '_NOUN']
        #     except:
        #         pass

        return float(cosine_similarity([vec1], [vec2])[0])

class Classifier(object):

    def __init__(self, resources_dir='resources/'):
        # Загружаем модель
        self.model = xgb.XGBClassifier()
        booster = pickle.load(open("xgboost_model", "rb"))
        self.model = booster


    def extract_features(self, obj):

        features = np.zeros(8)#obj.copy()
        filename = 'ruwikiruscorpora_upos_skipgram_300_2_2018.vec'
        model = KeyedVectors.load_word2vec_format(filename, binary=False)
        for itr in [0,1,2,3]:
            li = [2,4,6,8][itr]
            # print(obj[li],type(str(obj[li])))
            features[itr] = cnt_days(str(obj[li]))
            print(features[itr])
            print(features)
        for itr in [4,5,6,7]:
            li = [1,3,5,7][itr - 4]
            print(obj[li], type(obj[li]),'obj[li]')
            print((obj[0]), type((obj[0])), 'obj[0]')
            features[itr] = dist_betw_sent((obj[0]), (obj[li]), model)
            print(features[itr])
            print(features)


        # np.delete(features, 0, 1)
        # print(np.array(features).reshape((1,-1)))
        print('extract_features')
        print(type(features),'type feats')
        print(features.astype(float).reshape((1,-1)), 'type feats')
        return list([features, features])#features.astype(float).reshape((1,-1))


    def predict(self, obj):
        print(obj, type(obj))
        # Применение модели
        return self.model.predict_proba(self.extract_features(obj))[0][1]#self.extract_features(obj)