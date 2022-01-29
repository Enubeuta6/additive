from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', login, name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('generate/', generatepromo.as_view(), name='generate'),
]

handler404 = pageNotFound