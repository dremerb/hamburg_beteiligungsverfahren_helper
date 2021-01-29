import logging
import sys
from flask import Flask, abort
from flask import request
import pandas as pd
from clustering.clustergenerator import AffinityClusterGenerator, KMeansClusterGenerator
from clustering.config import PATH_TO_MODEL
from clustering.service import ClusterService
from clustering.featuregenerator import Word2VecFeatureGenerator

app = Flask(__name__)


def logger_init():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(name)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    root_logger.addHandler(ch)


logger_init()

generator = Word2VecFeatureGenerator(PATH_TO_MODEL)
cluster_service = ClusterService(generator, [(AffinityClusterGenerator(), False), (KMeansClusterGenerator(), True)])


@app.route('/cluster', methods=['POST'])
def get_cluster():
    logger = logging.getLogger("Cluster-Service")
    cluster_count = -1
    if not request.json or not 'configuration' in request.json:
        abort(400)

    configuration = request.json['configuration']
    if "clusterCount" in configuration:
        cluster_count = int(configuration['clusterCount'])

    logger.info(f"Number of clusters: {cluster_count}")
    documents = request.json['documents']
    data = pd.DataFrame(documents)

    return cluster_service.get_cluster(data, cluster_count)
