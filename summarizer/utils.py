import pandas
from datetime import datetime
import codecs
import numpy


class Utils:
    def comment_reader(self, commentfile):
        # prepare a parser fot the dates in DB
        dparse = lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

        # Read all comments
        comments = pandas.read_csv(commentfile, sep=";", dtype={"Contribution ID": int, "Comment ID": int,
                                                                "Comment Subject": str, "Comment Text": str},
                                   parse_dates=[4], date_parser=dparse)
        # sometimes pandas reads trash data. Remove this here
        comments = comments.loc[:, ~comments.columns.str.contains('^Unnamed')]

        # Shorten column names
        comments.columns=["conID", "commID", "subj", "text", "time"]

        # Generate IDs for "answer to" question
        answerto = comments[["conID", "subj"]].copy()
        answerto["commTo"] = answerto["subj"].replace(to_replace=numpy.nan, value="")
        answerto["commTo"] = answerto["commTo"].str.replace("Antwort an Nr. ", "")

        # Drop unneccessary column
        answerto = answerto.drop(columns=["subj"])

        # Merge "answer to" data with comment data
        comments = pandas.DataFrame.merge(comments, answerto, on="conID")

        return comments

    def contribution_reader(self, contribfile):
        # prepare a parser fot the dates in DB
        dparse = lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        colTypeMapping = {
            "Node ID": int,
            "Category": str,
            "Rubric": str,
            "Rating": float,
            "Total": int,
            "votes": int,
            "Upvotes": int,
            "Downvotes": int,
            "Comments": int,
            "Title": str,
            "Contributiontext": str
        }

        # Read all comments
        contributions = pandas.read_csv(contribfile, sep=";", dtype=colTypeMapping,
                                   parse_dates=[3], date_parser=dparse)
        contributions.columns = ["id", "cat", "rubric", "rating", "total", "votes", "upv", "downv", "comments", "title",
                                 "text"]

        return contributions

    def get_except_words(self, file):
        with codecs.open(file, "r", encoding="utf8") as file:
            exceptwords = file.readlines()

        # remove random whitespaces and newlines
        exceptwords = [e.strip() for e in exceptwords]

        # turn all words to lower case
        exceptwords = list(map(lambda w: w.lower(), exceptwords))
        return exceptwords
