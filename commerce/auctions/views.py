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
        bid = Bid(title=product, initial=initial)
        bid.save()

        # Placing listing in a table with the title provided by the products table and the bid provided by the bid table
        listing = Listing(title=product, description=description, url=url)
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
    query = Bid.objects.filter(title=listing.title).all()
    highest_bid = 0
    
    
    if request.method == "POST":
        if exists:
            if "remove" in request.POST:
                print("removing..." + str(exists))
                exists.delete()
            if "add" in request.POST:
                return HttpResponse("Error: Couldn't remove product.")
            else:
                pass
        elif not exists:
            if "add" in request.POST:
                print("adding...")
                username.save() 
                username.product.add(listing)
            if "remove" in request.POST:
                return HttpResponse("Error: Couldn't add product.")
            else: 
                pass
        
        # Gets the value provided by the user on the request, if value isn't valid it returns an error
        try:
            user_bid = int(request.POST["value"])
        except ValueError:
            return HttpResponse("Couldn't make a bid on the product. Enter a valid bid.")

        product = Product(product=str(listing.title))
        if not product:
            product.save()
        bid = Bid(title=product, offer=user_bid)
        
        if "bid" in request.POST:
            if user_bid > highest_bid:
                print("Saving...")
                print(str(bid))
                print(str(query))
                bid.save()
                bid.offer.add(user_bid)
                return HttpResponseRedirect(reverse("auctions:product", args=(product_id,)))
            else:
                return HttpResponse("Your bid must be superior to the highest bid.")
        
        for value in query:
            value = str(value)
            value = int(value)
            if value > highest_bid:
                highest_bid = value
            
    return render(request, "auctions/product.html", {
        "listing": Listing.objects.get(pk=product_id),
        "exists":exists,
        "highest_bid": highest_bid,
    })

def watchlist(request):
    print(str(Username.objects.filter(username=request.user.username).all()))
    return render(request, "auctions/watchlist.html", {
        "products":  Username.objects.filter(username=request.user.username).all(),
    })

