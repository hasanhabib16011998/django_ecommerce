from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Slider)
admin.site.register(Catagory)
admin.site.register(SubCatagory)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Condition)

class ProductAdmin(admin.ModelAdmin):
    list_display=('title','posted_by','created_at','updated_at')
admin.site.register(Product,ProductAdmin)
admin.site.register(SuperSubCatagory)
admin.site.register(Cart)
