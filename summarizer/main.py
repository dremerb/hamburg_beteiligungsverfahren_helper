import utils
import summarizer
import os


def main():
    util = utils.Utils()
    comments = util.comment_reader("demodata/2020-11-20 Jungfernstieg_Kommentare.csv")

    contributions = util.contribution_reader("demodata/2020-11-20 Jungfernstieg_Beiträge.csv")

    summer = summarizer.Summarizer(contributions["text"].values.tolist())

    # Words that do not deliver any content
    # These words are stored in txt databases in the folder "words"
    databases = os.listdir("words")
    exceptwords = []
    for db in databases:
        if db[-4:] == ".txt":
            exceptwords = exceptwords + (util.get_except_words("words/"+db))

    print(exceptwords)


    print(contributions["text"][52]+"\n\n")
    print(summer.get_words(contributions["text"][52], 10, exceptwords))


if __name__ == "__main__":
    main()