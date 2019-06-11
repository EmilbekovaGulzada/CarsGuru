from django.urls import path, re_path
from gigant.views import base_view, category_view, car_view, show_category, product_view, CategoryView, about_page, contacts_page
from gigant import views as core_views

urlpatterns = [
    # path('category/<str:slug>/', CategoryView.as_view(), name="product-detail"),
    # path('car/<slug:slug>/category/<slug:category_slug>/', show_category, name='category'),
    re_path(r'^car/(?P<slug>[\w-]+)(?:/category/(?P<category_slug>[\w-]+))?/$', CategoryView.as_view(), name='category'),
    path('product/<int:pk>/', product_view, name='product'),
    path('about/', about_page, name='about'),
    path('contacts/', contacts_page, name='contacts'),
    # path('activate/', core_views.activate, name='activate'),
    path('', base_view, name='base'),

]
