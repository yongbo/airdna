# coding: utf-8


import json
from urllib import urlencode
from urllib2 import urlopen

from flask import render_template, Blueprint, request

bp = Blueprint('search', __name__)


def NCBIsearch(**kwargs):

    HOST = "http://eutils.ncbi.nlm.nih.gov"
    SEARCH_URL = "{0}/entrez/eutils/esearch.fcgi/".format(HOST)
    SUMMARY_URL = "{0}/entrez/eutils/esummary.fcgi".format(HOST)

    print kwargs.get("query")
    search_args = {
            'db': kwargs.get("db", "pubmed"),
            'term': kwargs.get("term", 'PD1'),
            'retstart': kwargs.get("retstart", 0),
            'retmode': 'json',
            'sort': 'pub+date',
            }
    result = {"data": [], "totalCount": 0, "retstart": 0}
    try:
        data = urlopen(SEARCH_URL, urlencode(search_args)).read()
        data = json.loads(data)
        print data
        result["totalCount"] = int(data["esearchresult"]["count"])
        result["retstart"] = int(data["esearchresult"]["retstart"])
        ulist = ",".join(data["esearchresult"]["idlist"])
        data = urlopen(SUMMARY_URL, urlencode({"db": kwargs.get("db", "pubmed"), "id": ulist, 'retmode': 'json'})).read()
        data = json.loads(data)
        for x in data["result"]["uids"]:
            x = data["result"][x]
            result["data"].append({
                "id": x["uid"],
                "pub_date": x["epubdate"],
                "authors": x["authors"][0]["name"],
                "title": x["title"],
                "pub_journal": x["fulljournalname"],
                "pub_page": x["elocationid"]
                })
    except:
        pass
    return result
    

@bp.route('/search/', methods=['GET'])
def search():

    search_args = {
            'db': request.args.get("db", "pubmed"),
            'term': request.args.get("query", 'PD1'),
            'retstart': request.args.get("retstart", 0),
            'retmode': 'json'
            }
    data = NCBIsearch(**search_args)
    return render_template("site/searchNCBI.html", data = data)
