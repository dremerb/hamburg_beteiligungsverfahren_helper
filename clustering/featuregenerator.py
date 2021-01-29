from abc import ABC, abstractmethod

import nltk
import pandas as pd
from gensim.models import Doc2Vec
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

nltk.download('stopwords')

class FeatureGenerator(ABC):
    @abstractmethod
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class Word2VecFeatureGenerator(FeatureGenerator):

    def __init__(self, path_to_model):
        self.path_to_model = path_to_model
        self.model = Doc2Vec.load(path_to_model)

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df['feature_vector'] = df['body'].apply(self.generate_feature)
        return df

    def generate_feature(self, sentence):
        tokens = [t for t in simple_preprocess(sentence) if t not in stopwords.words('german')]
        return self.model.infer_vector(tokens)
