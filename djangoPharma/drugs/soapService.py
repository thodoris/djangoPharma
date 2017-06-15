import json

import drugs.utils as utils
from django.conf import settings
from suds.client import Client

# get soap wsdl endpoint from settings
client = Client(settings.DJANGOPHARMA_SOAP_URL,
                headers={'username': settings.WS_USERNAME,
                         'password': settings.WS_PASSWORD})


def get_all_drugs():
    response = client.service.fetchAllDrugs()
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


def get_drug_ids_and_names():
    response = client.service.getDrugIdsAndNames()
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


def get_drug_categories():
    response = client.service.getDrugCategories()
    # convert the xml to json
    json_data = utils.xml2json(response)
    drug_categories = json.loads(json_data)['drugCategory']
    return drug_categories


def search_drug(query):
    response = client.service.searchForDrugs(query)
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


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


def get_drug_by_category(category_id):
    response = client.service.fetchDrugsByCategory(category_id)
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


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

