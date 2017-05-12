from django.db import models

# Model for Category
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'
        managed = False


# Model for Drug
class Drug(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    barcode = models.TextField(max_length=512)
    price = models.DecimalField(decimal_places=2 , max_digits=3)
    availability = models.IntegerField()
    imagePath = models.URLField()
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'drugs'
        managed = False

    def get_price(self):
        return self.price

    def get_img_url(self):
        return self.imagePath
