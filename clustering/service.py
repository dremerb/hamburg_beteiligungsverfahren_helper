import logging

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

    def get_cluster(self, data: pd.DataFrame, num_cluster: int):
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
        return self.transfer_into_format(data)

    @staticmethod
    def transfer_into_format(data: pd.DataFrame):
        cluster = {}
        for index, row in data.iterrows():
            if row['cluster'] in cluster:
                cluster[row['cluster']].append(row['id'])
            else:
                cluster[row['cluster']] = [row['id']]
        return cluster
