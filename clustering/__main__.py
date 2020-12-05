import logging
import sys
from argparse import ArgumentParser
import os
import numpy as np
from sklearn.manifold import TSNE
from clustering.clustergenerator import Clustergenerator, AffinityClusterGenerator
from clustering.dataloader import DataLoader, FileLoader, ExcelDataLoader
from clustering.featuregenerator import Word2VecFeatureGenerator
from sklearn.cluster import AffinityPropagation
import pandas as pd
import matplotlib.pyplot as plt


def logger_init():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(name)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    root_logger.addHandler(ch)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', metavar='FILE', default='config.toml', help='config file')
    args = parser.parse_args()
    return args

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def main():
    cluster_set = []
    data_directory = "../summarizer/demodata/"
    for file in os.listdir(data_directory):
        loader = FileLoader.file_mapping()[file.split(".")[-1]](data_directory + file)
        if file.endswith('.xlsx') or "Beiträge" in file:
            continue

        data = loader.get_data()
        generator = Word2VecFeatureGenerator("german.model")
        cluster_generator = AffinityClusterGenerator()

        data = generator.generate_features(data)
        data = cluster_generator.generate_clusters(data)

        # Visualization
        feature_vectors = pd.DataFrame(data['feature_vector'].tolist())
        tsne = TSNE(n_components=2, random_state=0, n_iter=5000, perplexity=2)
        t = tsne.fit_transform(feature_vectors)
        clusters = data['cluster'].tolist()

        cmap = get_cmap(len(data['cluster'].unique().tolist()))
        plt.figure(figsize=(12, 6))
        for cluster, x, y in zip(clusters, t[:, 0], t[:, 1]):

            plt.scatter(x, y, c=cmap(cluster), edgecolors='r')
            if cluster in cluster_set:
                plt.annotate("", xy=(x + 1, y + 1), xytext=(0, 0), textcoords='offset points')
            else:
                plt.annotate(cluster, xy=(x + 1, y + 1), xytext=(0, 0), textcoords='offset points')
                cluster_set.append(cluster)
        plt.show()
        data.to_csv(f"cluster_{file}")



if __name__ == '__main__':
    main()
