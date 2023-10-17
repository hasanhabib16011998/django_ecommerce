from django.urls import path
from .views import *

urlpatterns = [
    path('',Home,name='Home'),
    path('search/',product_search_view,name='product_search_view'),
    path('super_sub_prod/<int:id>',super_sub_prod,name='super_sub_prod'),

]