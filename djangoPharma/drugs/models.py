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
    drug_id = models.CharField(max_length=40)
    friendly_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    availability = models.IntegerField()
    imagePath = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'drugs'
        managed = False

    def get_img_url(self):
        return self.imagePath
