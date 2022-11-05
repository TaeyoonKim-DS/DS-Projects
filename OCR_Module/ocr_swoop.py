## Import Libs

from paddleocr import PaddleOCR, draw_ocr
import pandas as pd
import numpy as np
import re
import string
import itertools
import nltk
from sklearn.metrics import roc_auc_score


class CharacterModel():
    def __init__(self, data, product_id, logger, targets):
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
        
    def create_temporary_directory(self):
        self.tmp_dir = tempfile.mkdtemp()
        os.mkdir(self.tmp_dir + "/images")
        self.logger.info("Character recognition temporary directories created")
        
    def get_image_hashes(self):
        data = self.data.copy()
        data = data[data["image"].notna()]
        data = data[~data["image"].isin(["empty"])]

        hash_set = set(data["image"].tolist())

        self.hash_lists["prediction_hashes"] = list(hash_set)
        self.logger.info("Compiled image hash list for Character recognition")
        
    def get_next_image_batch(self):
        self.hash_lists["prediction_hashes_batch"] = self.hash_lists["prediction_hashes"][:constants.OCR_BATCH_SIZE]
        self.hash_lists["prediction_hashes"] = self.hash_lists["prediction_hashes"][constants.OCR_BATCH_SIZE:]
        
    def add_prediction_images_to_directories(self):
        ai_functions.parallel_download_images_from_s3(
                                self.hash_lists["prediction_hashes_batch"],
                                (self.tmp_dir + "/images"))
        
    def check_prediction_directories_for_corrupt_images(self):
        directories = [self.tmp_dir + "/images"]
        ai_functions.delete_corrupt_images(directories, self.logger)
        self.logger.info("OCR directories checked for corrupt image files.")


    def check_the_prediction_directory_contains_images(self):
        return len([name for name in os.listdir(self.tmp_dir+"/images")])
        
    def get_words_and_scores_and_add_to_dataframe(self, row): # To do this, need to make a dataframe and apply
        photo = row["image"]
        if photo == "empty":
            return [[],[]]
        self.image_path = "/home/studio-lab-user/DS-Projects/OCR/SWOOP_OCR_image_test/{}.jpg".format(photo)
        self.result = self.ocr_model.ocr(self.image_path)
        self.texts = [res[1][0] for res in self.result]
        self.scores = [res[1][1] *100 for res in self.result]
        self.final_result = [self.texts, self.scores]
        
        return self.final_result
    
     
    def get_prediction_results(self):
        prediction_results_batch = pd.DataFrame() # At some point we need to make a dataframe
        prediction_results_batch['image'] = self.hash_lists["prediction_hashes_batch"]
        prediction_results_batch['OCR_score'] = prediction_results_batch.apply(self.score_extraction, axis=1)

        self.prediction_results = pd.concat([self.prediction_results, prediction_results_batch])
        
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
    
    def empty_prediction_folder(self):
        dir = (self.tmp_dir + "/images")
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
            
    def get_ocr_score(self):
        self.data["OCR_score"] = self.data.apply(self.get_final_score, axis=1)
        
    def get_roc_auc_score(self):
        
        roc_auc_scores = roc_auc_score(self.data['relevant'], self.data['OCR_score'])
        self.roc_auc_score = roc_auc_scores
        print("roc_auc_score: ", self.roc_auc_score)

        

        

    
    
    
    
        