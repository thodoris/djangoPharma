from django.shortcuts import render
from django.http import HttpResponse

from suds.client import Client
import utils


client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')


def index(request):
    output = '<h1>Index</h1>'
    return HttpResponse(output)


def detail(request,drug_id):
    response= utils.xml2json(client.service.findDrug(drug_id))
    return HttpResponse(response)


def get_drug(drugid):
    return client.service.findDrug(drugid)


# Create your views here.
