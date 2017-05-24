from suds.client import Client
from django.conf import settings
import drugs.utils as utils

#get soap wsdl endpoint from settings
client = Client(settings.DJANGOPHARMA_SOAP_URL)


def get_drug_ids_and_names():
    response = client.service.getDrugIdsAndNames()
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


def get_drug_categories():
    response = client.service.getDrugCategories()
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


def search_drug(query):
    response = client.service.searchForDrugs(query)
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


def get_drug(drug_id):
    response = client.service.findDrug(drug_id)
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data


def update_drug(request_data):
    response = client.service.updateDrug(request_data)
    # convert the xml to json
    json_data = utils.xml2json(response)
    return json_data
