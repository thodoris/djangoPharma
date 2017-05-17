from suds.client import Client
import drugs.utils as utils

client = Client('http://connect.opengov.gr:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')


# client = Client('http://localhost:8080/pharmacy-ws/PharmacyRepoWSImpl?wsdl')


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
