import drugs.soapService as soapService
from .models import Category
from django.db import IntegrityError, transaction

# Method for saving the drug categories in the local database
def migrate_drug_categories():
    # get from the WS the categories
    drug_categories = soapService.get_drug_categories()
    try:
        with transaction.atomic():
            for category in drug_categories:
                # save the drug category
                Category.objects.create(id=category['id'], name=category['name'])
    except IntegrityError:
        x = 0
