from django.conf.urls import url
from gigant.views import base_view, category_view, product_view


urlpatterns = [
    url{'', category/(?P<category_slug>[-\w]=)$', category_view, name='category_detile'),
    url{'',base_view, name='base'},

]