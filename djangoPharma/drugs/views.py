from django.shortcuts import render
from django.http import HttpResponse
import json
from suds.sudsobject import asdict
from suds.client import Client

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')

def recursive_dict(d):
    out = {}
    for k, v in asdict(d).items():
        if hasattr(v, '__keylist__'):
            out[k] = recursive_dict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(recursive_dict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out


def index(request):
    output = '<h1>Index</h1>'
    return HttpResponse(output)


def detail(request,drug_id):
    response= json.dumps(recursive_dict(client.service.findDrug(drug_id)))
    return HttpResponse(response)


def get_drug(drugid):
    return client.service.findDrug(drugid)


# Create your views here.
