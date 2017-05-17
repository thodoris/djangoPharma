from django.shortcuts import render
from django.http import HttpResponse

from suds.client import Client
from datetime import datetime
from .models import Drug, Category
from .forms import AddDrugsForm
import drugs.utils as utils
import drugs.restService as restService
import drugs.soapService as soapService

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')


# client = Client('http://localhost:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')


def index(request):
    output = '<h1>Index</h1>'
    return HttpResponse(output)


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
        # search_drug = soapService.search_drug('dep')
        # resp = restService.get_drugs()
        resp2 = restService.get_drug_by_id('000090201')
        form = AddDrugsForm()
    else:
        form = AddDrugsForm(request.POST)
        drug_id = request.POST.get('id')
        friendly_name = request.POST.get('friendlyName')
        description = request.POST.get('description')
        availability = request.POST.get('availability')
        # hardcoded value TODO Remove
        category_id = 100

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

# Create your views here.
