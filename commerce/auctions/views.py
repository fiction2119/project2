from typing import get_args
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Bid, Comment, Product, Username

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))

    return render(request, "auctions/index.html",   {
        "products": Product.objects.all(),
    })  

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["content"]
        initial = request.POST["initial"]
        url = request.POST["url"]
        
        product = Product(title=title, description=description, url=url, initial_bid=initial)
        product.save()
        
        # TODO: Current price changes in template.
        return render(request, "auctions/index.html", {
            "products": Product.objects.all(),
        })

    else:
        return render(request, "auctions/create.html")

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    username = Username(username=request.user.username, )
    highest_bid = 0
    username_check = Username.objects.filter(username=request.user.username)
    
    # Check if username exists, if not save the username provided
    if not username_check:
        print("saving username...")
        username.save()

    bid = Bid(bid=highest_bid, product_id=product_id)
    product_check = Bid.objects.filter(product_id=product_id)

    if not product_check:
        print("checking product...")
        bid.save()
        
    if request.method == "POST":
        title = product.title
        
        if "add" in request.POST:
            print(str(product_check))
        #if exists:
            #if "remove" in request.POST:
                #print("removing..." + str(exists))
                #exists.delete()
            #if "add" in request.POST:
                #return HttpResponse("Error: Couldn't remove product.")
        #elif not exists:
            #if "add" in request.POST:
                #print("adding..." + str(exists))
                #username.save() 
                #username.product.add(product)
            #if "remove" in request.POST:
                #return HttpResponse("Error: Couldn't add product.")
            
        # Gets the value provided by the user on the request, if value isn't valid it returns an error
        if "value" in request.POST:
            try:
                user_bid = int(request.POST["value"])
            except ValueError:
                return HttpResponse("Couldn't make a bid on the product. Enter a valid bid.")

        
    # TODO: Fix current price.
    return render(request, "auctions/product.html", {
        "product": product,
        
        "highest_bid": highest_bid,
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "products": None,
    })

