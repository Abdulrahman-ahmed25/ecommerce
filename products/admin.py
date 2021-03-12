from django.contrib import admin
from .models import Product, Variation, ProductImage, Category, ProductFeatured
# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
    list_display = [
        'sale_presentage',
    ]
    readonly_fields = ['sale_presentage',]
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'price',
    ]
    inlines = [
        VariationInline,
        ProductImageInline,
    ]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
# admin.site.register(Variation)
# admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)