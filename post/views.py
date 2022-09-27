
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import json
from taggit.models import Tag

from post.forms import UserRrgisterForm, UserLoginForm
from post.models import *


def index(request, tag_slug=None):
    query = None
    products = Product.objects.all()

    if "q" in request.GET:
        query = request.GET['q']
        products = products.filter(title__contains=query)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order ['get_cart_items']



    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__name__in=[tag])

    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, "pages/index.html", context)



def user_register(request):
    form = UserRrgisterForm()
    if request.method == "POST":
        form = UserRrgisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Account created successfully." , "success")
            return redirect("account:user_login")

    context = {'register_form': form}
    return render(request, "pages/register.html", context)


def user_login(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in your account." , "success")
                return redirect("account:user_cart")
            else:
                messages.error(request, "There is no account with this username.")
    context = {'login_form': form}
    return render(request, "pages/login.html", context)
    
@login_required
def user_logout(request):
    logout(request)
    return redirect("account:user_login")


@login_required
def user_cart (request): 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order ['get_cart_items']
    
    
       

    context = {'items': items , 'cartItems': cartItems,  'order':order}
    return render(request, "pages/cart.html", context)





def update_item (request): 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']



    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quanity = (orderItem.quanity + 1)
        messages.success(request, "Added to your cart" , "success")

    elif action == 'remove':
        orderItem.quanity = (orderItem.quanity - 1)
        messages.success(request, "Removed from your cart" , "success")

    elif action == 'delete':
        orderItem.quanity = (orderItem.quanity == 0)
        messages.success(request, "deleted from your cart" , "success")

    orderItem.save()

    if orderItem.quanity <= 0 :
        orderItem.delete()
        
    return JsonResponse('item was added', safe=False)


def category_view(request):
    tags = Tag.objects.all()
    context = {'tags' : tags}
    return render(request, 'pages/category_view.html' , context)