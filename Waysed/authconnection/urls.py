from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('generate/', generatepromo.as_view(), name='generate'),
    path('logout/', logout_user, name='logout'),
    path('profile', Profile.as_view(), name='profile'),
]

handler404 = pageNotFound