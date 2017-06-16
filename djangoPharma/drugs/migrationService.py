from decimal import Decimal

import drugs.cacheService as cacheService
import drugs.soapService as soapService
from django.db import transaction

from .models import Drug, Category


def synchronize_data():
    # get the drug categories from Cache
    if not cacheService.is_local_db_synchronized():
        drug_categories = cacheService.get_drug_categories()
        drugs = cacheService.get_all_drugs()
        try:
            with transaction.atomic():
                for category in drug_categories:
                    # save the drug category
                    obj, created = Category.objects.update_or_create(id=int(category['id']), defaults={
                        'name': category['name'], 'description': category['description']})
                    obj.save()
                for drug in drugs:
                    # save the drug category
                    obj, created = Drug.objects.update_or_create(id=drug['id'], defaults={
                        'category_id': int(drug['drugCategory']['id']),
                        'friendly_name': drug['friendlyName'], 'description': drug['description'],
                        'imagePath': drug['imagePath'], 'availability': int(drug['availability']),
                        'price': Decimal(drug['price'])})
                    obj.save()
                cacheService.set_local_db_synchronized(True)
                return True
        except Exception as e:
            cacheService.set_local_db_synchronized(False)
            return None
    return False


# Method for saving the drug categories in the local database
def migrate_drug_categories():
    # get from the WS the categories
    drug_categories = soapService.get_drug_categories()
    try:
        with transaction.atomic():
            for category in drug_categories:
                # save the drug category
                Category.objects.create(id=category['id'], name=category['name'])
    except Exception:
        x = 0
