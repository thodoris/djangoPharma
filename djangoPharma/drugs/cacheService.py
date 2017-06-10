import drugs.restService as restService
import drugs.soapService as soapService
import json
from django.core.cache import cache

CACHE_DRUGS_ALLDRUGS_KEY = 'DRUGS_ALLDRUGS'
CACHE_DRUGS_SINGLEDRUG_KEY = 'DRUGS_SINGLEDRUG_'
CACHE_DRUGS_INDEX_KEY = 'DRUGS_INDEX'


def __set_or_add(key,value,forceUpdate=False):
    if forceUpdate:
        cache.set(key, value)
    else:
        cache.add(key,value)


def __update_item_in_all_drugs_cache(item):
    itemid= item['id']
    key = CACHE_DRUGS_SINGLEDRUG_KEY +itemid
    all_drugs=get_all_drugs()
    for drug in all_drugs:
        drugid = drug['id']
        if drugid == itemid:
            drug = item
            __set_or_add(key, drug, True)
            __set_or_add(CACHE_DRUGS_ALLDRUGS_KEY, all_drugs, True)
            return
    all_drugs.append(item)
    __set_or_add(key, item, True)
    __set_or_add(CACHE_DRUGS_ALLDRUGS_KEY, all_drugs, True)


def get_drug(drugid, forceUpdate=False):
    try:
        key = CACHE_DRUGS_SINGLEDRUG_KEY + drugid
        drug= cache.get(key)
        if (drug is None or forceUpdate):
            drug = json.loads(soapService.get_drug(drugid))['drug'][0]
            if drugid != '':
                rest_data = restService.get_drug_by_id(drugid)
                drug['rest'] = rest_data
                __update_item_in_all_drugs_cache(drug)
        return drug
    except Exception as e:
        print('%s (%s)' % (e.message, type(e)))
        return None


def get_all_drugs(forceUpdate=False):
    try:
        drugs_data = cache.get(CACHE_DRUGS_ALLDRUGS_KEY)
        if (drugs_data is None or forceUpdate==True):
            drugs_data = json.loads(soapService.get_all_drugs())['drug']
            for drug in drugs_data:
                drugid = drug['id']
                if drugid != '':
                    rest_data = restService.get_drug_by_id(drugid)
                    drug['rest'] = rest_data
                    __set_or_add(CACHE_DRUGS_SINGLEDRUG_KEY + drugid, drug,forceUpdate)
            __set_or_add(CACHE_DRUGS_ALLDRUGS_KEY,drugs_data,forceUpdate)
        return drugs_data
    except:
        return None


def get_rest_drugs():
    try:
        rest_index = cache.get(CACHE_DRUGS_INDEX_KEY)
        if (rest_index is None):
            rest_index = restService.get_drugs_index()
            __set_or_add(CACHE_DRUGS_INDEX_KEY, rest_index,True)
        return rest_index
    except:
        return None
