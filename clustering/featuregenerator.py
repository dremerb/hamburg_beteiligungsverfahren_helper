from abc import ABC, abstractmethod
import pandas as pd
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from gensim.utils import simple_preprocess

class FeatureGenerator(ABC):
    @abstractmethod
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class Word2VecFeatureGenerator(FeatureGenerator):
    counter = 0

    def __init__(self, path_to_model, train=False):
        self.path_to_model = path_to_model
        self.should_train = train
        self.model = None

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df['TokenEmbedding'] = df['Comment Text'].apply(self.generate_tagged_document)
        model = Doc2Vec(df['TokenEmbedding'], vector_size=50, min_count=2, epochs=40)
        self.model = model
        df['feature_vector'] = df['Comment Text'].apply(self.generate_feature)
        return df

    @staticmethod
    def generate_tagged_document(line):
        tokens = simple_preprocess(line)
        Word2VecFeatureGenerator.counter += 1
        return TaggedDocument(tokens, [Word2VecFeatureGenerator.counter])

    def generate_feature(self, sentence):
        tokens = simple_preprocess(sentence)
        return self.model.infer_vector(tokens)

    def train(self):
        print(f"Not yet implemented: {self.train}")
