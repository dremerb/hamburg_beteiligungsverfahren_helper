import pandas as pd
from sklearn.cluster import AffinityPropagation


class Clustergenerator:

    def __init__(self, feature_generator, cluster_calculator):
        self.feature_generator = feature_generator
        self.cluster_calculator = cluster_calculator

    def generate_clusters(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class AffinityClusterGenerator:
    def generate_clusters(self, df: pd.DataFrame) -> pd.DataFrame:
        feature_vectors = pd.DataFrame(df['feature_vector'].tolist())
        df['cluster'] = AffinityPropagation(random_state=5).fit(feature_vectors).labels_
        return df
