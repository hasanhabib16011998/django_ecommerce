from django.urls import path
from .views import *

urlpatterns = [
    path('',Home,name='Home'),
    path('search/',product_search_view,name='product_search_view'),

]