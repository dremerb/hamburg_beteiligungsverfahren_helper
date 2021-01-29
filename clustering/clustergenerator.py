import pandas as pd
from sklearn.cluster import AffinityPropagation, KMeans


class ClusterGenerator:

    def generate_clusters(self, df: pd.DataFrame, num_cluster: int) -> pd.DataFrame:
        pass


class KMeansClusterGenerator:

    def generate_clusters(self, df: pd.DataFrame, num_cluster: int) -> pd.DataFrame:
        feature_vectors = pd.DataFrame(df['feature_vector'].tolist())
        df['cluster'] = KMeans(random_state=5, n_clusters=num_cluster).fit(feature_vectors).labels_
        return df


class AffinityClusterGenerator:

    def generate_clusters(self, df: pd.DataFrame, num_cluster: int) -> pd.DataFrame:
        feature_vectors = pd.DataFrame(df['feature_vector'].tolist())
        df['cluster'] = AffinityPropagation(random_state=5).fit(feature_vectors).labels_
        return df
