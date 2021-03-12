from django.shortcuts import render
from products.models import ProductFeatured,Product
# Create your views here.
def home_view(request):

    featured_image = ProductFeatured.objects.filter(active=True).order_by("?").first()
    products_recommended = Product.objects.filter(active=True).order_by("?")[:6]
    products_featured = Product.objects.filter(active=True).order_by("?")[:8]
    context = {
        "featured_image": featured_image,
        "products_recommended": products_recommended,
        "products_featured":products_featured,
    }
    return render(request, "home/home.html", context)