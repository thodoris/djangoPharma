import drugs.models as DrugModel
from django.contrib.auth.models import User
from django.db import models


class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.TextField(max_length=100, blank=True)
    streetno = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    zip = models.CharField(max_length=5, blank=True)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserAddress.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.useraddress.save()


STATUS_ENUM = (
    (1, 'Pending'),
    (2, 'Submitted'),
    (3, 'Ready For Delivery'),
    (4, 'Delivered'),
    (5, 'Rejected'),
)

PAYMENT_TYPE_ENUM = {
    (1, 'Cash'),
    (2, 'Bank Disposal')
}

SHIPMENT_TYPE_ENUM = {
    (1, 'From Store'),
    (2, 'Courier')
}


# Model for Order
class Order(models.Model):
    user = models.ForeignKey(User)
    address = models.ForeignKey(UserAddress)
    order_date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_ENUM, default=1)
    payment_type = models.IntegerField(choices=PAYMENT_TYPE_ENUM, default=1)
    shipment_type = models.IntegerField(choices=SHIPMENT_TYPE_ENUM, default=1)
    comments = models.CharField(max_length=500)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'orders'

    def get_payment_type(self):
        return self.payment_type


# Model for Order Details
class OrderDetails(models.Model):
    order = models.ForeignKey(Order)
    drug = models.ForeignKey(DrugModel.Drug)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'orders_details'
