from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserDataMeta(AbstractUser):


    email = models.EmailField(max_length=254, null=True)
    selectorpromo = models.ForeignKey('PromocodeData', on_delete=models.CASCADE, null=True)
    credit = models.IntegerField(default=0)


    REQUIRED_FIELDS = ['email',]
    USERNAME_FIELD = 'login'
    is_anonymous = False
    is_authenticated = True


    def __str__(self):
        return self.login


class PromocodeData(models.Model):
    promoCode = models.TextField(max_length=32)
    linkedTo = models.CharField(max_length=32)

    def __str__(self):
        return self.promoCode