from django.urls import path
from gigant.views import base_view, category_view, car_view, show_category
from gigant import views as core_views



urlpatterns = [
    path('car/<slug:car_slug>/category/<slug:category_slug>/', show_category, name='category'),
    path('car/<slug:car_slug>/', car_view, name='car_detail'),
    path('activate/', core_views.activate, name='activate'),
    path('',base_view, name='base'),

]



