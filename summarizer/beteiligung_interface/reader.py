import requests
import json


def get_contributions_with_meta(verfahrensname):
    response = requests.get(
        f"https://beteiligung.hamburg/{verfahrensname}/drupal/de/masterportal/layer/contributions?SERVICE=GeoJSON&REQUEST=GetCapabilities")
    # print(response.json())

    contributions = []
    for f in response.json()["features"]:
        # remove the "link" key, keep only "nid", "name", "Thema" and "Rubric"
        f["properties"].pop("link", None)
        # save the contribution
        contributions.append(f["properties"])

    return contributions


def get_contributions(verfahrensname):
    contribs = get_contributions_with_meta(verfahrensname)
    returnlist = []
    for c in contribs:
        returnlist.append(c["description"])

    return returnlist


def get_contributions_count(verfahrensname):
    list = get_contributions(verfahrensname)
    return len(list)
