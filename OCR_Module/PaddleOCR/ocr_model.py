from paddleocr import PaddleOCR, draw_ocr
import pandas as pd
import numpy as np
import re
import string
import itertools
import nltk
from sklearn.metrics import roc_auc_score


class CharacterModel():

    def __init__(self, targets):
        self.ocr_model = None
        self.data = None
        self.image_path = None
        self.result = None
        self.text = None
        self.scores = None
        self.result = None
        self.final_result = None
        self.targets = targets
        
        
    def define_model(self):
        self.ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
    
    def import_data(self):
        self.data = pd.read_csv("image_relevant_.csv", encoding='latin')
        self.data = self.data[['image', 'relevant']]

    def get_words_and_scores_and_add_to_dataframe(self, row):
        photo = row["image"]
        if photo == "empty":
            return [[],[]]
        self.image_path = "/home/studio-lab-user/DS-Projects/OCR/SWOOP_OCR_images/{}.jpg".format(photo)
        self.result = self.ocr_model.ocr(self.image_path)
        self.texts = [res[1][0] for res in self.result]
        self.scores = [res[1][1] *100 for res in self.result]
        self.final_result = [self.texts, self.scores]
        
        return self.final_result

    def get_text_score(self):
        self.data["words"] = self.data.apply(self.get_words_and_scores_and_add_to_dataframe, axis=1)
    
    def new_score_text(self, row):
        sample_list = row["words"][0]
        score_list = row["words"][1]
        new_text = []
        new_score = []
        
        for text, score in zip(sample_list, score_list): # assign text and score each
            new_text.extend(text.split()) #update new_text.
            number_of_space = text.count(" ") # number of spaces +1 is chunk of words
            for i in range(number_of_space+1):
                new_score.append(score)

        return [new_text, new_score]
    
    def get_new_score_text(self):
        self.data["words"] = self.data.apply(self.new_score_text, axis=1)
    
    def clean_text(self, row):
        word_list = row["words"][0]
        new_word_list = []
        for word in word_list:
            new_word = word.lower()
            new_word = re.sub("[%s]" % re.escape(string.punctuation), " ", new_word)
            new_word_list.append(new_word)
        return [new_word_list, row["words"][1]]
    
    def get_clean_text(self):
        self.data["words"] = self.data.apply(self.clean_text, axis=1)
        
    def advance(self, iterator, step):
        next(itertools.islice(iterator, step, step), None)

    def tuplewize(self, iterable, size):
        iterators = itertools.tee(iterable, size)
        for position, iterator in enumerate(iterators):
            self.advance(iterator, position)
        return zip(*iterators)

    def get_final_score(self, row):
        sample_list = row["words"][0]
        score_list = row["words"][1]
        max_score = 0

        for target in self.targets:
            phrase_length = len(target.split())
            for i in range(1, phrase_length+1):
                for c, s in zip(self.tuplewize(sample_list, i), self.tuplewize(score_list, i)):
                    new_sample = " ".join(c)
                    edit_distance = nltk.edit_distance(target, new_sample)
                    closeness = (len(target)-edit_distance)/len(target)
                    confidence_score = np.mean(s)
                    final_score = closeness * confidence_score
                    if final_score > max_score:
                        max_score = final_score

        return max_score
    
    def get_ocr_score(self):
        self.data["OCR_score"] = self.data.apply(self.get_final_score, axis=1)
        
        
    def get_roc_auc_score(self):
        
        roc_auc_scores = roc_auc_score(self.data['relevant'], self.data['OCR_score'])
        self.roc_auc_score = roc_auc_scores
        print("roc_auc_score: ", self.roc_auc_score)

    def predict(self):
        self.define_model()
        self.import_data()
        self.get_text_score()
        self.get_new_score_text()
        self.get_clean_text()
        self.get_ocr_score()
        self.get_roc_auc_score()
        return print(self.data)