from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page
from suds.client import Client
from datetime import datetime
from .models import Drug, Category
from django.core import serializers
from .forms import AddDrugsForm, UpdateDrugsForm
import drugs.utils as utils
import drugs.restService as restService
import drugs.soapService as soapService
import drugs.cacheService as cacheService
import drugs.migrationService as migrationService
import json

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')
CACHE_TTL = getattr(settings, 'DJANGOPHARMA_CACHE_TTL', DEFAULT_TIMEOUT)


# client = Client('http://localhost:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')

def __getDrugAsModel(drug_id):
    newdrug = Drug()
    jsondrug = cacheService.get_drug(drug_id)
    drug = Drug.fromjson(newdrug, jsondrug)
    return drug


def index(request):
    output = '<h1>Index</h1>'
    return HttpResponse(output)


def test(request):
    drugs_data = cacheService.get_all_drugs()
    if drugs_data is not None:
        context = {'data': drugs_data}
        return render(request, 'app/test.html', context)
    else:
        return render(request, 'app/error.html', {'error': 'Cannot get data', }, content_type='application/xhtml+xml')


def detail(request, drug_id):
    # drug = Drug.objects.get(pk=drug_id)
    drug = __getDrugAsModel(drug_id)
    context = {'drug': drug}
    return render(request, 'app/drug_details.html', context)


def get_drug(drugid):
    return client.service.findDrug(drugid)


def add_drug(request):
    if request.method == 'GET':
        # get the drug IDS from the external Rest Service
        drugs_index = cacheService.get_rest_drugs()
        id_choices = [(drug['id'], drug['name']) for drug in drugs_index]
        form = AddDrugsForm(choices=id_choices)
    elif request.method == 'POST':
        drugs_index = cacheService.get_rest_drugs()
        id_choices = [(drug['id'], drug['name']) for drug in drugs_index]
        form = AddDrugsForm(request.POST, choices=id_choices)
        if form.is_valid():
            # save the drug
            drug = form.save()
            # send to the SOAP WS for the insert
            soapService.insert_drug(drug)
        else:
            return HttpResponse('invalid')

    return render(request, 'app/addDrug.html', {
        'form': form,
        'title': 'Add new Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    })


def update_drug(request, drug_id):
    update_succeed = None
    if request.method == 'GET':
        # get the info from the SOAP WS
        # drug = Drug.objects.get(pk=drug_id)
        drug = __getDrugAsModel(drug_id)
        selected_drug = soapService.get_drug(drug_id)
        # get drug categories
        drug_categories = soapService.get_drug_categories()

        # json_data = json.loads(selected_drug)
        # model = json_data['drug'][0]
        # drug_id = model['id']
        # friendly_name = model['friendlyName']
        # description = model['description']
        # availability = model['availability']
        # category_id = model['drugCategory']['id']
        form = UpdateDrugsForm(instance=drug)
    elif request.method == 'POST':
        # get the drug
        drug = Drug.objects.get(pk=drug_id)
        form = UpdateDrugsForm(request.POST, instance=drug)
        if form.is_valid():
            # send to the SOAP WS for the update
            updated_drug = soapService.update_drug(drug)
            if updated_drug is None:
                update_succeed = False
            else:
                # save the model
                form.save()
                update_succeed = True
        else:
            update_succeed = False

    return render(request, 'app/updateDrug.html', {
        'form': form,
        'title': 'Update Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
        'result': update_succeed
    })


def manage_migrations(request):
    migrationService.migrate_drug_categories()
