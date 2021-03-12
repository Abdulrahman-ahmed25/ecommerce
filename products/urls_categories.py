from django.urls import path
from .views import CategoryListView, CategoryDetailView


app_name='categories'
urlpatterns = [
    path('', CategoryListView.as_view(), name='categories'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category_details'),
    # path('<int:pk>/inventory/', VariationListView.as_view(), name='product_inventory'),


]