import requests
import json


BASEURL = "https://beteiligung.hamburg/domainmodul-test/drupal/dipas-pds"


def get_all_contributions_with_meta(projid):
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions")
    # print(response.json())

    contributions = []
    for f in response.json()["features"]:
        contributions.append(f["properties"])

    return contributions


def get_all_contributions(projid, title=False):
    contribs = get_all_contributions_with_meta(projid)
    returnlist = []
    for c in contribs:
        if title:
            returnlist.append(c["title"] + " " + c["contributionContent"])
        else:
            returnlist.append(c["contributionContent"])

    return returnlist


def get_all_comments_of_contrib(projid, contribid):
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions/{contribid}/comments")

    comments = []
    for contrib in response.json()["features"]:
        for comment in contrib["properties"]["comments"]:
            comments.append(comment["commentContent"])

    return comments


def get_all_commented_contributions(projid, title=False):
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
    response = requests.get(f"{BASEURL}/projects/{projid}/contributions/{contribid}")

    j = response.json()["features"][0]["properties"]
    if title:
        return j["title"] + " " + j["contributionContent"]
    else:
        return j["contributionContent"]


def get_contribution_with_comments(projid, nid):
    contrib = get_contribution(projid, nid)
    comments = get_all_comments_of_contrib(projid, nid)
    comstr = ""
    for com in comments:
        comstr = comstr + " " + com
    # comstr has leading " "
    return contrib + comstr


def get_contributions_count(projid):
    list = get_all_contributions(projid)
    return len(list)