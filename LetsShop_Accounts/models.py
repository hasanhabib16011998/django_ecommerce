from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, verbose_name=("User Profile"), on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class Address(models.Model):
    address_type=models.CharField(max_length=50,null=True,blank=True)
    user=models.ForeignKey(User, verbose_name=("Address"), on_delete=models.CASCADE)
    company=models.CharField(max_length=100)
    company_address=models.CharField(max_length=50,null=True,blank=True)
    town=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    phone=models.TextField()

    def __str__(self):
        return str(f'{self.user.username},{self.company}')