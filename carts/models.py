from decimal import Decimal
from django.db import models
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from products.models import Variation
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title
    def get_title(self):
        return f'{self.item.product.title} - {self.item.title}'
    
    # def add_to_cart(self):
    #     return 0
    def remove(self):
        return f'{reverse("cart")}?item={self.item.id}&delete=True'

# to calculate the line_item_total
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if Decimal(qty) >= 1 :
        price = instance.item.get_price()
        line_item_total = Decimal(price) * Decimal(qty)
        instance.line_item_total = line_item_total
        
pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

# to calculate the subtotal
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.updated_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

class Cart(models.Model):
    #user
    #items
    #timetemp
    #updated
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True,)
    items = models.ManyToManyField(Variation, through=CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.id)
    
    def updated_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()
