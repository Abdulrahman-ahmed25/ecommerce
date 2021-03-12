from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils import text
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        products_one = self.get_queryset().filter(category__in=instance.category.all())
        products_two = self.get_queryset().filter(default=instance.default)
        qs = (products_one | products_two).exclude(id = instance.id).distinct()
        return qs


class Product(models.Model):
    title = models.CharField(max_length=120)
    description =models.TextField(blank=True, null=True)
    price =models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #category and default
    category = models.ManyToManyField('Category', blank=True)
    default  = models.ForeignKey('Category',on_delete=models.CASCADE, related_name='default_category', null=True, blank=True)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #     through='Comment', related_name='comments_owned')
    
    # # Favorites
    # favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #     through='Fav', related_name='favorite_ads')
    objects = ProductManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_details", kwargs = {"pk": self.pk})

    #for getting image from db
    def get_image_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img #None
# class Fav(models.Model) :
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
#     class Meta:
#         unique_together = ('product', 'user')

#     def __str__(self) :
#         return '%s likes %s'%(self.user.username, self.product.title[:10])

# class Comment(models.Model) :

#     text = models.TextField(
#     validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")])

#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # # Shows up in the admin list
    # def __str__(self):
    #     if len(self.text) < 15 : return self.text
    #     return self.text[:11] + ' ...'

import math
class Variation(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False, null=False)
    price =models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    sale_price =models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title   
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
    def get_price(self):
        if self.sale_price is not "None":
            return self.sale_price
        else:
            return self.price

    #to make calculated field
    def get_sale_presentage(self):
        if self.sale_price is not None:
            sale_presentage = round((1 - (self.sale_price/self.price))*100)
            return sale_presentage
    sale_presentage = property(get_sale_presentage)


    def get_html_price(self):
        if self.sale_price is not None:
            # sale = round(((1 -(int(self.sale_price)/(self.price)))*100),1)
            # print(sale)
            html_text = f"<span>EGP {int(self.sale_price)} <small>{int(self.price)}</small></span><p style=' width:auto; color:red;background-color: hsla(14, 100%, 53%, 0.2);font-size:14px'>-{self.sale_presentage}%</p>"
        else:
            html_text = f"<span>EGP {int(self.price)}</span>"
        return mark_safe(html_text)

    
def product_post_saved_receiver(sender, instance,created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

post_save.connect(product_post_saved_receiver, sender=Product)

def image_upload_to(instance, filename):
    title = instance.product.title
    slug  = slugify(title)
    file_extension = filename.split(".")
    # new_filename = "%s-%s.%s" %(slug, instance.id, file_extension) = 
    new_filename = f'{slug}-{instance.id}.{file_extension}' 
    return f'Product/{slug}/{new_filename}'

class ProductImage(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to = image_upload_to)

    def __str__(self):
        return self.product.title


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug  = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    time_published = models.DateTimeField(auto_now_add=True, auto_now=False)
    image =  models.ImageField(upload_to = 'images/', null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categories:category_details", kwargs = {"slug": self.slug})
        
class ProductFeatured(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   image   = models.ImageField(upload_to='featured')
   title   = models.CharField(max_length=120, null=False, blank=False)
   text    = models.CharField(max_length=300, null=True, blank=True)
   text_right = models.BooleanField(default=False)
   show_price = models.BooleanField(default=False)
   make_image_background = models.BooleanField(default=True)
   text_css_color = models.CharField(max_length=50, default="white")
   active  = models.BooleanField(default=True) 

   def __str__(self):
       return self.product.title