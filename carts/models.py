from django.db import models
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from products.models import Variation
# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.item.title

class Cart(models.Model):
    #user
    #items
    #timetemp
    #updated
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True,)
    items = models.ManyToManyField(Variation, through=CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)