from django.shortcuts import render
from django.http import HttpResponse

from suds.client import Client
from datetime import datetime
from .models import Drug, Category
from .forms import AddDrugsForm
import utils

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


def insert_drug(drug):
    # request_data = client.factory.create('addDrug')
    # request_data.id = drug.id
    response = client.service.addDrug(id=drug.id, name=drug.name, price=drug.price, availability=drug.availability,
                                      categoryid=1)
    return HttpResponse(response)


def add_drug(request):
    if request.method == 'GET':
        form = AddDrugsForm()
    else:
        form = AddDrugsForm(request.POST)
        id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        barcode = request.POST.get('barcode')
        price = request.POST.get('price')
        availability = request.POST.get('availability')
        # hardcoded value
        category = Category(id=1)
        post = Drug(id=id, name=name, description=description, barcode=barcode, price=price,
                    availability=availability, category=category)
        insert_drug(post)
        # if form.is_valid():
        #     id = form.cleaned_data['id']
        #     name = form.cleaned_data['name']
        #     description = form.cleaned_data['description']
        #     barcode = form.cleaned_data['barcode']
        #     price = form.cleaned_data['price']
        #     availability = form.cleaned_data['availability']
        #     categoryid = 1
        #     post = Drug.objects.create(id=id, name=name, description=description, barcode=barcode, price=price,
        #                                availability=availability, categoryId=categoryid, userId=request.user)
        #     insert_drug(post)
        #     return HttpResponseRedirect("/posts/" + str(post.id))

    return render(request, 'app/addDrug.html', {
        'form': form,
        'title': 'Add new Drug',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    })

# Create your views here.
