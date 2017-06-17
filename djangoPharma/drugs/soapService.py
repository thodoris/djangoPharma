import json

import drugs.utils as utils
from django.conf import settings
from suds.client import Client

# get soap wsdl endpoint from settings (use WS Authentication)
client = Client(settings.DJANGOPHARMA_SOAP_URL,
                headers={'username': settings.WS_USERNAME,
                         'password': settings.WS_PASSWORD})


# get all drugs
def get_all_drugs():
    response = client.service.fetchAllDrugs()
    if response.ResponseCode == 'C':
        # convert the xml to json
        json_data = utils.xml2json(response)
        return json_data
    else:
        return None


# get drug categories
def get_drug_categories():
    response = client.service.getDrugCategories()
    if response.ResponseCode == 'C':
        # convert the xml to json
        json_data = utils.xml2json(response)
        drug_categories = json.loads(json_data)['drugCategory']
        return drug_categories
    else:
        return None


# get drug
def get_drug(drug_id):
    response = client.service.findDrug(drug_id)
    if response.ResponseCode == 'C':
        # convert the xml to json
        json_data = utils.xml2json(response)
        obj = json.loads(json_data)['drug']
        # WS returns a list of Drugs - for this call it will be always 1 element
        return obj[0]
    else:
        return None


# add drug
def insert_drug(drug):
    # create the request for the WS
    request_data = {'id': drug.id, 'friendlyName': drug.friendly_name,
                    'availability': drug.availability,
                    'description': drug.description,
                    'price': str(drug.price),
                    'categoryId': drug.category.id,
                    'imagePath': drug.imagePath}
    response = client.service.addDrug(request_data)
    if response.ResponseCode == 'C':
        # convert the xml to json
        json_data = utils.xml2json(response)
        obj = json.loads(json_data)['drug']
        # WS returns a list of Drugs - for this call it will be always 1 element
        return obj[0]
    else:
        return None


# update drug
def update_drug(drug):
    # create the request for the WS
    request_data = {'id': drug.id, 'friendlyName': drug.friendly_name,
                    'availability': drug.availability,
                    'description': drug.description,
                    'price': str(drug.price),
                    'categoryId': drug.category.id}
    response = client.service.updateDrug(request_data)
    if response.ResponseCode == 'C':
        # convert the xml to json
        json_data = utils.xml2json(response)
        obj = json.loads(json_data)['drug']
        # WS returns a list of Drugs - for this call it will be always 1 element
        return obj[0]
    else:
        return None


# insert drug category
def insert_drug_category(category):
    # create the request for the WS
    request_data = {'id': category.id, 'name': category.name,
                    'description': category.description}
    response = client.service.addDrugCategory(request_data)
    # the response does not contain the drug category
    if response.ResponseCode == 'C':
        return True
    else:
        return False


# update drug category
def update_drug_category(category):
    # create the request for the WS
    request_data = {'id': category.id, 'name': category.name,
                    'description': category.description}
    response = client.service.updateDrugCategory(request_data)
    # the response does not contain the drug category
    if response.ResponseCode == 'C':
        return True
    else:
        return False
