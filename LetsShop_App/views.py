from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from sslcommerz_lib import SSLCOMMERZ 


# Create your views here.
def Home(request):
    user=request.user
    if user:
        cart=Cart.objects.filter(user=user)
        len_cart=len(cart)
        if cart:
            total=0
            for i in cart:
                total_amount=(i.quantity)*(i.product.current_price)
                total= total+total_amount
    print(cart)
    slides=Slider.objects.all()
    products=Product.objects.all()
    feature_prod=products.filter(featured_product=True)

    return render(request,'Home.html',locals())

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

def add_to_cart(request,id):
    user=request.user
    prod=Product.objects.get(id=id)

    if user.is_authenticated:
        try:
            cart=Cart.objects.get(Q(user=user,product=prod))
            cart.quantity+=1
            cart.save()
            return redirect('Home')

        except Cart.DoesNotExist:
            cart=Cart.objects.create(user=user,product=prod)
            cart.save()
            return redirect('Home')
        
def remove_cart(request,id):
    user=request.user
    cart=Cart.objects.get(Q(user=user,id=id))
    cart.delete()
    return redirect('Home')

def cart_page(request):
    user=request.user
    if user:
        cart=Cart.objects.filter(user=user)
        len_cart=len(cart)
        if cart:
            total=0
            for i in cart:
                total_amount=(i.quantity)*(i.product.current_price)
                total= total+total_amount
                ship_total=total+75
    return render(request,'Product/cart_page.html',locals())

def increase(request,id):
    user=request.user
    cart=Cart.objects.get(Q(user=user,product=id))
    cart.quantity+=1
    if cart.quantity>cart.product.quantity:
        messages.warning(request,'Sorry,Product quantity not available.')
        return redirect('cart_page')
    cart.save()
    return redirect('cart_page')

def decrease(request,id):
    user=request.user
    cart=Cart.objects.get(Q(user=user,product=id))
    cart.quantity-=1
    if cart.quantity==0:
        cart.delete()
    cart.save()
    return redirect('cart_page')

def sslcommerz_payment(request):
    user=request.user
    if user:
        cart=Cart.objects.filter(user=user)
        len_cart=len(cart)
        if cart:
            total=0
            for i in cart:
                total_amount=(i.quantity)*(i.product.current_price)
                total= total+total_amount
                ship_total=total+75
    

    sslcz = { 'store_id': 'testbox', 'store_pass': 'qwerty', 'issandbox': True }
    post_body = {}
    post_body['total_amount'] = 100.26
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = "your success url"
    post_body['fail_url'] = "your fail url"
    post_body['cancel_url'] = "your cancel url"
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print(response)
    # Need to redirect user to response['GatewayPageURL']