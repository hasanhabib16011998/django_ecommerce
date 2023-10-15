from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def Home(request):
    slides=Slider.objects.all()

    return render(request,'Home.html',{'slides':slides})

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
            if catagory:
                product=products.filter(catagory=catagory)
            if sub_catagory:
                product=products.filter(sub_catagory=sub_catagory)
            if color:
                product=products.filter(color=color)
            if size:
                product=products.filter(size=size)
            if condition:
                product=products.filter(condition=condition)
    
    except Exception as e:
        messages.warning(request,'No product Available.')

        
        



    return render(request,'Product/search.html',locals())
             