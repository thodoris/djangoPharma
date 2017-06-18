from decimal import Decimal

import drugs.cacheService as cacheService
import drugs.soapService as soapService
from django.db import transaction

from .models import Drug, Category


# synchronize local DB with the Store (SOAP)
# updates the cache
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
                        'imagePath': drug['imagePath'] if 'imagePath' in drug else 'default_drug_image.png', 'availability': int(drug['availability']),
                        'price': Decimal(drug['price'])})
                    obj.save()
                cacheService.set_local_db_synchronized(True)
                return True
        except Exception as e:
            cacheService.set_local_db_synchronized(False)
            return None
    return False


