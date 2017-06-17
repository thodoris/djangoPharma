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
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from suds.client import Client

from .forms import AddDrugsForm, UpdateDrugsForm, AddDrugCategoryForm, UpdateDrugCategoryForm
from .models import Drug, Category

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')
CACHE_TTL = getattr(settings, 'DJANGOPHARMA_CACHE_TTL', DEFAULT_TIMEOUT)

# get a drug from the cache and return it as a Model Drug item
def __getDrugAsModel(drug_id):
    newdrug = Drug()
    jsondrug = cacheService.get_drug(drug_id)
    drug = Drug.fromjson(newdrug, jsondrug)
    return drug

# get a drug category from the cache and return it as a Model Category item
def __getDrugCategoryAsModel(category_id):
    newcategory = Category()
    jsondrugcategory = cacheService.get_drug_category(int(category_id))
    category = Category.fromjson(newcategory, jsondrugcategory)
    return category


def __getCategoryChoices():
    # get the drug categories from Cache
    drug_categories = cacheService.get_drug_categories()
    category_choices = [(int(category['id']), category['name']) for category in drug_categories]
    return category_choices

# returns a dictionary with all available (REST API) drugs
# Dict item contains drug id & drug name from the REST API
def __getDrugIDsChoices():
    # get the drug IDS from Cache
    drugs_index = cacheService.get_rest_drugs()
    id_choices = [(drug['id'], drug['name']) for drug in drugs_index]
    return id_choices


# check if the logged in user is the admin
def check_admin(user):
    return user.is_superuser


# returns the drug details
def detail(request, drug_id):
    drug = __getDrugAsModel(drug_id)
    context = {'drug': drug,
               'image_path': '/static/app/images/drugs/' + drug.imagePath}
    return render(request, 'drugs/drug_details.html', context)

# add drug view
@user_passes_test(check_admin)
def add_drug(request):
    insert_succeed = None
    if request.method == 'GET':
        id_choices = __getDrugIDsChoices()
        category_choices = __getCategoryChoices()
        form = AddDrugsForm(categorychoices=category_choices, category=None)
    elif request.method == 'POST':
        id_choices = __getDrugIDsChoices()
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


# update drug view
@user_passes_test(check_admin)
def update_drug(request, drug_id):
    update_succeed = None
    if request.method == 'GET':
        # get drug info from Cache
        drug = __getDrugAsModel(drug_id)
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
                # update the cache
                cacheService.get_drug(drug.id, True)  # passing True to forceUpdate parameter , updates the cache
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

# list of drug categories
@user_passes_test(check_admin)
def display_drug_categories(request):
    categories = Category.objects.all()
    return render(request, 'app/admin/drugCategoriesList.html', dict(categories=categories))

# add drug categories
@user_passes_test(check_admin)
def add_drug_category(request):
    if request.method == 'GET':
        form = AddDrugCategoryForm()
        return render(
            request,
            'app/admin/addDrugCategory.html',
            {
                'form': form,
                'title': 'Add Drug Category',
                'year': datetime.now().year,
            }
        )
    elif request.method == 'POST':
        form = AddDrugCategoryForm(request.POST)
        insert_succeed = None
        if form.is_valid():
            try:
                with transaction.atomic():
                    category = form.save()
                    inserted_drug_category = soapService.insert_drug_category(category)
                    if inserted_drug_category is False:
                        raise Exception
                    else:
                        cacheService.get_drug_categories(True)  # True forces update of cache from Soap
                        # go to list page
                        request.method = 'GET'
                        return display_drug_categories(request, category.id)
            except Exception:
                insert_succeed = False

        return render(
            request,
            'app/admin/addDrugCategory.html',
            {
                'form': form,
                'title': 'Add Drug Category',
                'year': datetime.now().year,
                'result': insert_succeed
            }
        )


# update drug category
@user_passes_test(check_admin)
def update_drug_category(request, drug_category_id):
    update_succeed = None
    if request.method == 'GET':
        drug_category = __getDrugCategoryAsModel(drug_category_id)
        form = UpdateDrugCategoryForm(instance=drug_category)
    elif request.method == 'POST':
        # get the drug category
        drug_category = Category.objects.get(pk=drug_category_id)
        form = UpdateDrugCategoryForm(request.POST, instance=drug_category)
        if form.is_valid():
            # send to the SOAP WS for the update
            updated_drug_category = soapService.update_drug_category(drug_category)
            if updated_drug_category is None:
                update_succeed = False
            else:
                # save the model
                form.save()
                # update the cache
                cacheService.get_drug_category(drug_category.id,
                                               True)  # passing True to forceUpdate parameter , updates the cache
                update_succeed = True
        else:
            update_succeed = False

    return render(
        request,
        'app/admin/updateDrugCategory.html',
        {
            'form': form,
            'title': 'Update Drug Category',
            'year': datetime.now().year,
            'result': update_succeed
        }
    )


# the image for the drug will be one of the static images in the application, random each time
def get_random_image_for_drug():
    drug_images_nums = ['000840105', '023280101', '038260201', '041670301', '093360302',
                        '099880107', '175990402']
    drug_number = random.choice(drug_images_nums)
    return drug_number + '.png'

# ListView view with the drugs that belong to a specific category
class CategoryDrugsList(ListView):
    template_name = 'drugs/drugs_by_category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.args[0])
        return Drug.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryDrugsList, self).get_context_data(**kwargs)
        context['category_name'] = self.category.name
        context['category_desc'] = self.category.description
        return context
