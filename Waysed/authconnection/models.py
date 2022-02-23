from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserDataMeta(AbstractUser):

    credit = models.IntegerField(default=0)



    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = True


    def __str__(self):
        return self.username


class PromoDataMeta(models.Model):
    code_key = models.CharField(max_length=32)
    linkedto = models.ForeignKey('UserDataMeta', on_delete=models.CASCADE, null=True,)


    def __str__(self):
        return self.code_key
