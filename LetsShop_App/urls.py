from django.urls import path
from .views import *

urlpatterns = [
    path('',Home,name='Home'),
    path('search/',product_search_view,name='product_search_view'),
    path('super_sub_prod/<int:id>',super_sub_prod,name='super_sub_prod'),
    path('add_to_cart/<int:id>/',add_to_cart,name='add_to_cart'),
    path('remove_cart/<int:id>/',remove_cart,name='remove_cart'),
    path('cart_page/',cart_page,name='cart_page'),
    path('decrease/<int:id>/',decrease,name='decrease'),
    path('increase/<int:id>/',increase,name='increase'),

]