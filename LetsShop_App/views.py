from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def Home(request):
    slides=Slider.objects.all()
    products=Product.objects.all()
    feature_prod=products.filter(featured_product=True)

    return render(request,'Home.html',{'slides':slides,'feature_prod':feature_prod})

def product_search_view(request):
    try:
        form=ProductSearchForms(request.GET)
        products=Product.objects.all()

        if form.is_valid():
            query=form.cleaned_data.get('query')
            catagory=form.cleaned_data.get('catagory')
            sub_catagory=form.cleaned_data.get('sub_catagory')
            color=form.cleaned_data.get('color')
            size=form.cleaned_data.get('size')
            condition=form.cleaned_data.get('condition')
            if query:
                product=products.objects.filter(Q(title__icontains=query))
            elif catagory:
                product=products.filter(catagory=catagory)
            elif sub_catagory:
                product=products.filter(sub_catagory=sub_catagory,catagory=catagory)
            elif color:
                product=product.filter(color=color)
            elif size:
                product=product.filter(size=size)
            elif condition:
                product=product.filter(condition=condition)
    
    except Exception as e:
        messages.warning(request,'No product Available.')
        return redirect('product_search_view')

    return render(request,'Product/search.html',locals())

def super_sub_prod(request,id):
    prod=Product.objects.filter(super_sub_catagory=id)
    return render(request,'Product/super_sub_prod.html',locals())
             