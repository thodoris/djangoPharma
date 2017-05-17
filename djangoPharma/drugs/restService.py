import json
from urllib.request import urlopen

rest_api = 'http://test.hua.gr:8000/pharmacy'


def get_drugs():
    json_data = json.load(urlopen(rest_api))
    return json_data


def get_drug_by_id(drug_id):
    urlpath = rest_api + '/' + drug_id
    resp = json.load(urlopen(urlpath))
    return resp
