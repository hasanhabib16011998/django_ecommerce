from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


def logedin_user():
    from django.contrib.auth import get_user
    return get_user()
# Create your models here.
class Slider(models.Model):
    title=models.CharField(max_length=50)
    title1=models.CharField(max_length=50)
    description=models.TextField()
    button_tag=models.CharField(max_length=20)
    image=models.ImageField(upload_to='slider_image/')

    def __str__(self):
        return str(self.title)
    
class Catagory(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)

class SubCatagory(models.Model):
    title=models.CharField(max_length=50)
    catagory=models.ForeignKey(Catagory, verbose_name=(""), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)+'|'+str(self.catagory)
    
class SuperSubCatagory(models.Model):
    title=models.CharField(max_length=50)
    SubCatagory=models.ForeignKey(SubCatagory, verbose_name=(""), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
    
class Size(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)

class Color(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)

class Condition(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)
    
class Product(models.Model):
 
    posted_by=models.ForeignKey(User,default=logedin_user, verbose_name=("Posted By"), on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    catagory=models.ForeignKey(Catagory, verbose_name=("Catagories"), on_delete=models.CASCADE)
    sub_catagory=models.ForeignKey(SubCatagory, verbose_name=("Sub-Catagory"), on_delete=models.CASCADE)
    super_sub_catagory=models.ForeignKey(SuperSubCatagory, verbose_name=("Super-Sub-Catagory"), on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to='Product_image1/')
    image2=models.ImageField(upload_to='Product_image2/')
    image3=models.ImageField(upload_to='Product_image3/')
    current_price=models.DecimalField(max_digits=10,decimal_places=2)
    prev_price=models.DecimalField(max_digits=10,decimal_places=2)
    short_description=models.TextField()
    color=models.ManyToManyField(Color)
    size=models.ManyToManyField(Size)
    top_seller=models.BooleanField(default=False)
    deals_of_the_day=models.BooleanField(default=False)
    trending_product=models.BooleanField(default=False)
    featured_product=models.BooleanField(default=False)
    condition=models.ManyToManyField(Condition)
    quantity=models.PositiveIntegerField()
    wish_list=models.BooleanField(default=False)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Cart(models.Model):
 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(f'{self.user} Cart')
    
    def total_price(self):
        return self.quantity*self.product.current_price
    
    def total_quantity(self):
        return Cart.objects.filter(user=self.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0