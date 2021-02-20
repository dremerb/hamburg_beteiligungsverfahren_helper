import requests
import json


BASEURL = "https://beteiligung.hamburg/domainmodul-test/drupal/dipas-pds"


def get_all_contributions_with_meta(projid):
    """
    Gets raw data from contributions with all fields in the "properties" section of a feature
    :param projid: id of the project containing contributions
    :return: list of dictionaries containing contribution data
    """
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions")
    # print(response.json())

    contributions = []
    for f in response.json()["features"]:
        contributions.append(f["properties"])

    return contributions


def get_all_contributions(projid, title=False):
    """
    Gets raw contribution contents.
    :param projid: ID of the project
    :param title: Switch if contribution title should be prepended to result
    :return: the contribution's text (with prepended title, if title set True)
    """
    contribs = get_all_contributions_with_meta(projid)
    returnlist = []
    for c in contribs:
        if title:
            returnlist.append(c["title"] + " " + c["contributionContent"])
        else:
            returnlist.append(c["contributionContent"])

    return returnlist


def get_all_comments_of_contrib(projid, contribid):
    """
    Pulls all comments for a specific contribution
    :param projid: ID of the project
    :param contribid: ID of the contribution
    :return: list of comments (text only)
    """
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions/{contribid}/comments")

    comments = []
    for contrib in response.json()["features"]:
        for comment in contrib["properties"]["comments"]:
            comments.append(comment["commentContent"])

    return comments


def get_all_commented_contributions(projid, title=False):
    """
    Get a list of strings consisting of the comment and appended comments
    :param projid: ID of the project
    :param title: Switch if contribution title should be prepended to result
    :return: String containing contribution and comment text
    """
    response = requests.get(f"{BASEURL}/projects/{projid}/commentedcontributions")

    result = []
    for c in response.json()["features"]:
        if title:
            contrib = c["properties"]["title"] + " " + c["properties"]["contributionContent"]
        else:
            contrib = c["properties"]["contributionContent"]
        comments = ""
        for com in c["properties"]["commentedBy"]:
            comments = comments + com["commentContent"]

        result.append(contrib + " " + comments)
    return result


def get_contribution(projid, contribid, title=False):
    """
    Get a single contribution (text only)
    :param projid: ID of the project
    :param contribid: ID of the contribution
    :param title: Switch if contribution title should be prepended to result
    :return: Text of a contribution
    """
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions/{contribid}")

    j = response.json()["features"][0]["properties"]
    if title:
        return j["title"] + " " + j["contributionContent"]
    else:
        return j["contributionContent"]


def get_contribution_with_meta(projid, contribid):
    """
    Get the raw data for a single contribution, as returned from the API
    :param projid: ID of the project
    :param contribid: ID of the contribution
    :return: Dictionary containing return value from API
    """
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions/{contribid}")
    return response.json()["features"][0]["properties"]


def get_contribution_with_comments(projid, nid, title=False):
    """
    Get a string containing comment text and appended comment texts
    :param projid: ID of the project
    :param nid: ID of the contribution
    :param title: Switch if contribution title should be prepended to result
    :return: String consisting of a contribution's text and appended comments
    """
    contrib = get_contribution(projid, nid, title)
    comments = get_all_comments_of_contrib(projid, nid)
    comstr = ""
    for com in comments:
        comstr = comstr + " " + com
    # comstr has leading " "
    return contrib + comstr


def get_contributions_count(projid):
    """
    Count all contributions in a project
    :param projid: ID of the project
    :return: int, number of contributions
    """
    list = get_all_contributions(projid)
    return len(list)