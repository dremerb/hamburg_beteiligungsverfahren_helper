import logging
from typing import Dict

from sklearn.feature_extraction.text import CountVectorizer

from clustering.featuregenerator import Word2VecFeatureGenerator
import pandas as pd


class NoAlgorithmFoundError(Exception):
    def __init__(self, message):
        super(NoAlgorithmFoundError, self).__init__(message)


class ClusterService:
    def __init__(self, feature_generator: Word2VecFeatureGenerator,
                 cluster_generators):
        self.cluster_generators = cluster_generators
        self.feature_generator = feature_generator
        self.logger = logging.getLogger("Cluster-Service")

    def get_cluster(self, data: pd.DataFrame, num_cluster: int) -> Dict:
        final_cluster_generator = None
        for cluster_generator, supports_num_cluster in self.cluster_generators:
            if num_cluster >= 0:
                if supports_num_cluster:
                    final_cluster_generator = cluster_generator
            if num_cluster == -1:
                if not supports_num_cluster:
                    final_cluster_generator = cluster_generator

        self.logger.info(f"Choosing {type(final_cluster_generator).__name__} to generate cluster")

        if not final_cluster_generator:
            raise NoAlgorithmFoundError(
                f"There is no algorithm for {num_cluster} in place. Only options are"
                f" {[type(generator).__name__ for generator, _ in self.cluster_generators]}")

        data = self.feature_generator.generate_features(data)
        data = final_cluster_generator.generate_clusters(data, num_cluster)
        keywords = self.get_keywords(data)
        return self.transfer_into_format(data, keywords)

    @staticmethod
    def get_keywords(data: pd.DataFrame, num_keywords=3) -> Dict:
        keywords = {}
        groups = data.groupby("cluster")
        cv = CountVectorizer(max_features=2000)
        for cluster_id, group in groups:
            print(group['body'])
            cv.fit_transform(group['body'])
            keywords[cluster_id] = list(cv.vocabulary_.keys())[:num_keywords]
        return keywords

    @staticmethod
    def transfer_into_format(data: pd.DataFrame, keywords: Dict) -> Dict:
        cluster = {}
        for index, row in data.iterrows():
            topics = ",".join(keywords[row["cluster"]])
            if topics in cluster:
                cluster[topics].append(row["id"])
            else:
                cluster[topics] = [row["id"]]
        return cluster
