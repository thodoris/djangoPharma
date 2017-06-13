import random
from datetime import datetime

import drugs.cacheService as cacheService
import drugs.migrationService as migrationService
import drugs.soapService as soapService
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from suds.client import Client

from .forms import AddDrugsForm, UpdateDrugsForm
from .models import Drug

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')
CACHE_TTL = getattr(settings, 'DJANGOPHARMA_CACHE_TTL', DEFAULT_TIMEOUT)


# client = Client('http://localhost:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')

def __getDrugAsModel(drug_id):
    newdrug = Drug()
    jsondrug = cacheService.get_drug(drug_id)
    drug = Drug.fromjson(newdrug, jsondrug)
    return drug


def __getCategoryChoices():
    # get the drug categories from Cache
    drug_categories = cacheService.get_drug_categories()
    category_choices = [(int(category['id']), category['name']) for category in drug_categories]
    return category_choices


def __getDrugIDsChoices():
    # get the drug IDS from Cache
    drugs_index = cacheService.get_rest_drugs()
    id_choices = [(drug['id'], drug['name']) for drug in drugs_index]
    return id_choices


def check_admin(user):
    return user.is_superuser


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
    drug = __getDrugAsModel(drug_id)
    context = {'drug': drug,
               'image_path': '/static/app/images/drugs/' + drug.imagePath}
    return render(request, 'app/drug_details.html', context)


def get_drug(drugid):
    return client.service.findDrug(drugid)


@user_passes_test(check_admin)
def add_drug(request):
    insert_succeed = None
    if request.method == 'GET':
        id_choices = __getDrugIDsChoices()
        category_choices = __getCategoryChoices()
        form = AddDrugsForm(categorychoices=category_choices, category=None)
    elif request.method == 'POST':
        id_choices = __getDrugIDsChoices()
        category_choices = __getCategoryChoices()

        form = AddDrugsForm(request.POST, categorychoices=None, category=None)

        # the function checks also if there is another record with the same id
        if form.is_valid():
            try:
                with transaction.atomic():
                    # save the drug
                    drug = form.save()
                    # save the random image
                    random_image_path = get_random_image_for_drug()
                    drug.imagePath = random_image_path
                    # update only image field
                    drug.save(update_fields=["imagePath"])
                    # send to the SOAP WS for the insert
                    inserted_drug = soapService.insert_drug(drug)
                    if inserted_drug is None:
                        raise Exception
                    else:
                        # force update the cache
                        cacheService.get_drug(drug.id, True)
                        # go to detail page
                        return detail(request, drug.id)
            except Exception:
                insert_succeed = False

    return render(request, 'app/admin/addDrug.html', {
        'form': form,
        'title': 'Add new Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
        'result': insert_succeed,
        'idchoices': id_choices
    })


@user_passes_test(check_admin)
def update_drug(request, drug_id):
    update_succeed = None
    if request.method == 'GET':
        # get drug info from Cache
        drug = __getDrugAsModel(drug_id)
        # get drug categories
        category_choices = __getCategoryChoices()
        form = UpdateDrugsForm(instance=drug, categorychoices=category_choices)
    elif request.method == 'POST':
        # get the drug
        drug = Drug.objects.get(pk=drug_id)
        form = UpdateDrugsForm(request.POST, instance=drug, categorychoices='')
        if form.is_valid():
            # send to the SOAP WS for the update
            updated_drug = soapService.update_drug(drug)
            if updated_drug is None:
                update_succeed = False
            else:
                # save the model
                form.save()
                # update the cache
                cacheService.get_drug(drug.id, True)
                update_succeed = True
        else:
            update_succeed = False

    return render(request, 'app/admin/updateDrug.html', {
        'form': form,
        'title': 'Update Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
        'result': update_succeed
    })


@user_passes_test(check_admin)
def manage_migrations(request):
    migrationService.synchronize_data()
    return HttpResponse(200)


# the image for the drug will be one of the static images in the application, random each time
def get_random_image_for_drug():
    drug_images_nums = ['000840105', '023280101', '038260201', '041670301', '093360302',
                        '099880107', '175990402']
    drug_number = random.choice(drug_images_nums)
    return drug_number + '.png'
