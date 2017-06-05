from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page
from suds.client import Client
from datetime import datetime
from .models import Drug
from django.core import serializers
from .forms import AddDrugsForm, UpdateDrugsForm
import drugs.utils as utils
import drugs.restService as restService
import drugs.soapService as soapService
import json

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')
CACHE_TTL = getattr(settings, 'DJANGOPHARMA_CACHE_TTL', DEFAULT_TIMEOUT)


# client = Client('http://localhost:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')


def index(request):
    output = '<h1>Index</h1>'
    return HttpResponse(output)


@cache_page(CACHE_TTL)
def test(request):
    drugs_data = json.loads(soapService.get_all_drugs())['drug']
    for drug in drugs_data:
        drugid = drug['id']
        if drugid != '':
            rest_data = restService.get_drug_by_id(drugid)
            drug['rest'] = rest_data
    return HttpResponse(drugs_data)


def detail(request, drug_id):
    response = utils.xml2json(client.service.findDrug(drug_id))
    return HttpResponse(response)


def get_drug(drugid):
    return client.service.findDrug(drugid)


def insert_drug(request_data):
    response = client.service.addDrug(request_data)

    return HttpResponse(response)


def add_drug(request):
    if request.method == 'GET':
        drugs_info = soapService.get_drug_ids_and_names()
        drug_categories = soapService.get_drug_categories()
        obj_generator = serializers.deserialize("json", drug_categories)
        # search_drug = soapService.search_drug('dep')
        all_drugs = ''  # restService.get_drugs()
        resp2 = restService.get_drug_by_id('000090201')
        form = AddDrugsForm(drug_categories=drug_categories, all_drugs=all_drugs)
    else:
        form_class = AddDrugsForm
        drug_categories = soapService.get_drug_categories()
        form = form_class(data=request.POST, drug_categories=drug_categories, all_drugs='')

        if form.is_valid():
            drug_id = request.POST.get('drug_id', '')
            friendly_name = request.POST.get('friendly_name', '')
            description = request.POST.get('description', '')
            availability = request.POST.get('availability', '')
            category_id = request.POST.get('category', '')
        else:
            form.errors
            return HttpResponse('invalid')

        request_data = {'id': drug_id, 'friendlyName': friendly_name, 'availability': availability,
                        'description': description,
                        'categoryId': category_id}

        insert_drug(request_data)
        #     return HttpResponseRedirect("/posts/" + str(post.id))

    return render(request, 'app/addDrug.html', {
        'form': form,
        'title': 'Add new Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    })


def update_drug(request, drug_id):
    if request.method == 'GET':
        # get the info from the SOAP WS
        selected_drug = soapService.get_drug(drug_id)
        # get drug categories
        drug_categories = soapService.get_drug_categories()

        json_data = json.loads(selected_drug)
        model = json_data['drug'][0]
        drug_id = model['id']
        friendly_name = model['friendlyName']
        description = model['description']
        availability = model['availability']
        category_id = model['drugCategory']['id']

        drug = Drug(drug_id=drug_id, friendly_name=friendly_name, description=description, availability=availability)

        form = UpdateDrugsForm(instance=drug, drug_categories=drug_categories, initial={'category_id': category_id})
    else:
        form_class = UpdateDrugsForm
        drug_categories = soapService.get_drug_categories()
        form = form_class(data=request.POST, drug_categories=drug_categories, initial={'category_id': ''})

        if form.is_valid():
            drug_id = request.POST.get('drug_id', '')
            friendly_name = request.POST.get('friendly_name', '')
            description = request.POST.get('description', '')
            availability = request.POST.get('availability', '')
            category_id = request.POST.get('category', '')
        else:
            form.errors
            return HttpResponse('invalid')

        request_data = {'id': drug_id, 'friendlyName': friendly_name, 'availability': availability,
                        'description': description,
                        'categoryId': category_id}

        soapService.update_drug(request_data)

    return render(request, 'app/updateDrug.html', {
        'form': form,
        'title': 'Update Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    })


# Create your views here.