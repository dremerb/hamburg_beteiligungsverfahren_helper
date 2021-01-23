# https://stackabuse.com/text-summarization-with-nltk-in-python/

from nltk import tokenize
from nltk import corpus
import re
import heapq


SENTENCELENGTH = 150


def check_similar_words(words):
    """
    This function check for similar words, to remove e. g. "finde" and "finden", as they have the same meaning.
    Check for word length as a first heuristic, then check if one word contains the other => same.

    :param words: words to check
    :return: list of similar words in the input. Only the latter similar word is returned.
    """
    similar = []
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if abs(len(words[i]) - len(words[j])) < 3:              # if word length is similar
                if words[i] in words[j] or words[j] in words[i]:    # if one word is contained in the other
                    similar = similar + [words[j]]                    # mark as similar

    return similar


class Summarizer:
    def __init__(self, all_contribs):
        """
        Build a frequency table over all inputted contributions. Sets internal var self.freq_table

        :param all_contribs: contributions to use for frequency table building
        :return: nothing
        """
        # set up stopwords
        stopwords = set(corpus.stopwords.words("german"))
        # Make a huge text from all contributions for word freq analysis
        text = ""
        for c in all_contribs:
            if c[-1] == ".":
                text += c+" "
            else:
                text += c+". "

        # filter multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # remove all non-text stuff (e. g. newlines or '.', ',')
        contrib_formatted = re.sub(r"[^a-zA-Zäüöß]", " ", text)

        # get word frequency (lowercase words)
        self.freq_table = dict()
        lowercasewords = map(lambda w: w.lower(), tokenize.word_tokenize(contrib_formatted))
        for word in lowercasewords:   # for every word
            if word not in stopwords:                                    # that is not a stopword
                if len(word) > 3:                                        # filter short words (normally nor interesting)
                    if word not in self.freq_table.keys():               # add to frequency table
                        self.freq_table[word] = 1
                    else:
                        self.freq_table[word] += 1

        # get weighted frequency
        maxfreq = max(self.freq_table.values())
        for word in self.freq_table.keys():
            self.freq_table[word] = (self.freq_table[word]/maxfreq)

    def get_words(self, contrib, sumlen, exceptwords):
        """
        Get top words from a single contribution as a summary

        :param contrib: contribution to summarize
        :param sumlen: #words for summary
        :param exceptwords: words to exclude in summary
        :return: a summary of the contribution in the form of top rated words
        """
        # get words in contrib from freq_table (contrib to lower, as only lower in freq_table)
        words_in_contrib = tokenize.word_tokenize(contrib.lower())

        # build a local frequency table
        word_freq_table = dict()
        for word in words_in_contrib:
            if word in self.freq_table:
                # filter exceptwords here for efficiency
                if word in exceptwords:
                    continue
                word_freq_table[word] = self.freq_table[word]

        # get the top words
        words = heapq.nlargest(sumlen, word_freq_table, key=word_freq_table.get)

        similar = check_similar_words(words)
        while len(similar) > 0:
            words = heapq.nlargest(sumlen + len(similar), word_freq_table, key=word_freq_table.get)
            words = [w for w in words if w not in similar]
            similar = check_similar_words(words)

        return words
