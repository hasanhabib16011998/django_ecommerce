from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/',Login,name='Login'),
    path('registration/',Registration,name='Registration'),
    path('reset_password/',Reset_pass,name='Reset_pass'),
    path('logout/',Logout,name='Logout'),
    path('success/',Success,name='Success'),
    path('error/',Error,name='Error'),
    path('token_send/',Token,name='Token'),
    path('verify/<auth_token>',verify,name='verify'),
    path('Reset_user_pass/<auth_token>',Reset_user_pass,name='Reset_user_pass'),
    path('user_dashboard/',User_dash,name='User_dash'),

]
