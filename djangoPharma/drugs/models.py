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
    friendlyname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    availability = models.IntegerField()
    imagePath = models.URLField()
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'drugs'
        managed = False

    def get_img_url(self):
        return self.imagePath
