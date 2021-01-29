from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing
import os


# Hierfür braucht man einen wikipedia corpus dieser kann unter https://dumps.wikimedia.org/enwiki/ gefunden werden.

class TaggedWikiDocument(object):
    def __init__(self, wiki):
        self.wiki = wiki
        self.wiki.metadata = True

    def __iter__(self):
        for content, (page_id, title) in self.wiki.get_texts():
            yield TaggedDocument(content, [title])


if __name__ == '__main__':
    print("Wiki Corpus")
    wiki = WikiCorpus("wiki-corpus.xml.bz2")

    if os.path.exists("german.model"):
        os.remove("german.model")

    documents = TaggedWikiDocument(wiki)
    cores = multiprocessing.cpu_count()
    print("Starting with Doc2Vec")
    model = Doc2Vec(dm=0, dbow_words=1, size=200, window=8, min_count=19, iter=10, workers=cores)
    print("Building vocab")
    model.build_vocab(documents)
    print("Training")
    model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
    model.save("german.model")
