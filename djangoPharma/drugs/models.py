from decimal import Decimal

from django.db import models


# Model for Category
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'categories'

    def fromjson(self, json):
        self.id = int(json['id'])
        self.name = json['name']
        self.description = json['description']
        return self


# Model for Drug
class Drug(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    friendly_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    availability = models.IntegerField()
    imagePath = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'drugs'

    def get_img_url(self):
        return self.imagePath

    def fromjson(self, json):
        self.id = json['id']
        self.friendly_name = json['friendlyName']
        self.description = json['description']
        self.availability = int(json['availability'])
        self.imagePath = json['imagePath']
        self.price = Decimal(json['price'])
        newcategory = Category()
        jsoncategory = json['drugCategory']
        drugcategory = Category.fromjson(newcategory, jsoncategory)
        self.category = drugcategory
        return self
