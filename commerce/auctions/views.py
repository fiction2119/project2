from typing import get_args
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Product, Username

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))

    return render(request, "auctions/index.html",   {
        "listings": Listing.objects.all(),
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
        
        # Placing product in a table
        product = Product(product=title)
        product.save()

        # Placing bid in a table with the title provided by the products table
        bid = Bid(title=product, bid=initial)
        bid.save()

        # Placing listing in a table with the title provided by the products table and the bid provided by the bid table
        listing = Listing(title=product, bid=bid, description=description, url=url)
        listing.save()

        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
        })

    else:
        return render(request, "auctions/create.html")


def product(request, product_id):
    listing = Listing.objects.get(pk=product_id)
    username = Username(username=request.user.username)
    exists = Username.objects.filter(username=request.user.username, product=listing).all()

    if request.method == "POST":
        if exists:
            if "remove" in request.POST:
                print("removing..." + str(exists))
                exists.delete()
                
            if "add" in request.POST:
                return HttpResponse("Error: Couldn't remove product.")
        elif not exists:
            if "add" in request.POST:
                print("adding...")
                username.save() 
                username.product.add(listing)
            if "remove" in request.POST:
                return HttpResponse("Error: Couldn't add product.")

        bid = Bid.objects.get(title=listing.title)
        highest_bid = str(listing.bid)
        highest_bid = int(highest_bid)
        
        if "bid" in request.POST:
            if int(request.POST["value"]) > highest_bid:
                bid.bid.add(request.POST["value"])
        
        
        
        return HttpResponseRedirect(reverse("auctions:product", args=(product_id,)))
            
    return render(request, "auctions/product.html", {
        "product": listing,
        "exists":exists,
        "highest_bid": listing.bid,
    })

def bid(request, product_id):
    if request.method == "POST":
        
        
        
        return render(request, "auctions/product.html",{
            "highest_bid": listing.bid
        },)
    
    return render(request, "auctions/product.html", {
        "highest_bid": listing.bid
    }, args=(product_id,) )

def watchlist(request):
    print(str(Username.objects.filter(username=request.user.username).all()))
    return render(request, "auctions/watchlist.html", {
        "products":  Username.objects.filter(username=request.user.username).all(),
    })

