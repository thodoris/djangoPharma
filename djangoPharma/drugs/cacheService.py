import json

import drugs.restService as restService
import drugs.soapService as soapService
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'DJANGOPHARMA_CACHE_TTL', DEFAULT_TIMEOUT)

CACHE_DRUGS_ALLDRUGS_KEY = 'DRUGS_ALLDRUGS'
CACHE_DRUGS_SINGLEDRUG_KEY = 'DRUGS_SINGLEDRUG_'
CACHE_DRUGS_INDEX_KEY = 'DRUGS_INDEX'
CACHE_DRUGS_CATEGORIES_KEY = 'DRUGS_CATEGORIES'
CACHE_LOCALDB_SYNCHRONIZED_KEY = 'LOCALDB_SYNCHRONIZED'


def __set_or_add(key, value, forceUpdate=False):
    if forceUpdate:
        cache.set(key, value, CACHE_TTL)
    else:
        cache.add(key, value, CACHE_TTL)


def __update_item_in_all_drugs_cache(item):
    itemid = item['id']
    key = CACHE_DRUGS_SINGLEDRUG_KEY + itemid
    all_drugs = get_all_drugs()
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


def clear_cache():
    cache.clear()


def is_local_db_synchronized():
    is_sync = cache.get(CACHE_LOCALDB_SYNCHRONIZED_KEY, False) == True
    return is_sync


def set_local_db_synchronized(is_sync):
    cache.set(CACHE_LOCALDB_SYNCHRONIZED_KEY, is_sync, CACHE_TTL)


def get_drug(drugid, forceUpdate=False):
    try:
        key = CACHE_DRUGS_SINGLEDRUG_KEY + drugid
        drug = cache.get(key)
        if (drug is None or forceUpdate):
            drug = soapService.get_drug(drugid)
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
        if (drugs_data is None or forceUpdate == True):
            drugs_data = json.loads(soapService.get_all_drugs())['drug']
            for drug in drugs_data:
                drugid = drug['id']
                if drugid != '':
                    rest_data = restService.get_drug_by_id(drugid)
                    drug['rest'] = rest_data
                    __set_or_add(CACHE_DRUGS_SINGLEDRUG_KEY + drugid, drug, forceUpdate)
            __set_or_add(CACHE_DRUGS_ALLDRUGS_KEY, drugs_data, forceUpdate)
        return drugs_data
    except Exception as e:
        return None


def get_rest_drugs():
    try:
        rest_index = cache.get(CACHE_DRUGS_INDEX_KEY)
        if (rest_index is None):
            rest_index = restService.get_drugs_index()
            __set_or_add(CACHE_DRUGS_INDEX_KEY, rest_index, True)
        return rest_index
    except:
        return None


def get_drug_categories():
    try:
        categories_data = cache.get(CACHE_DRUGS_CATEGORIES_KEY)
        if (categories_data is None):
            categories_data = soapService.get_drug_categories()
            __set_or_add(CACHE_DRUGS_CATEGORIES_KEY, categories_data, True)
        return categories_data
    except:
        return None
