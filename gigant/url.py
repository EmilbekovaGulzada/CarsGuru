from django.urls import path
from gigant.views import base_view, category_view, product_view
# cart_view


urlpatterns = [
    path('category/<slug:category_slug>/', category_view, name='category'),
    path('product/<slug:product_slug>/', product_view, name='product_detail'),
    # path('', cart_view, name='cart'),
    path('',base_view, name='base'),


]