import codecs


def get_except_words(file):
    """
    Read the words that should be contained in the exception list
    :param file: input file
    :return: a list of all the words in the file
    """
    with codecs.open(file, "r", encoding="utf8") as file:
        exceptwords = file.readlines()

    # remove random whitespaces and newlines
    exceptwords = [e.strip() for e in exceptwords]

    # turn all words to lower case
    exceptwords = list(map(lambda w: w.lower(), exceptwords))
    return exceptwords
