from django.db import models


# Model for Category
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'


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
