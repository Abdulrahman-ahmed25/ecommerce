from django.contrib import admin
from django.db import models
from django.db.models.base import Model
from .models import Cart, CartItem
# Register your models here.

class CartItemInline(admin.TabularInline):
    model= CartItem
    extra = 1
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline
    ]
    class Meta:
        Model= Cart

admin.site.register(Cart, CartAdmin)