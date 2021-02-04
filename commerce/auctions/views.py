from typing import get_args
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Transaction, User, Bid, Comment, Product, Username, Watchlist, Category

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
        category = request.POST["category"]

        category = Category.objects.get(category=category)

        product = Product(title=title, description=description, url=url, initial_bid=initial,seller=request.user.username, category=category)
        product.save()
        
        return render(request, "auctions/index.html", {
            "products": Product.objects.all(),
        }) 

    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
        })

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    # Check if current user is the seller of the product
    if request.user.username == product.seller:
        seller = True
    else:
        seller = False
    
    
    # Check if current logged in username exists, if not save it
    if Username.objects.filter(username=request.user.username):
        username = Username.objects.get(username=request.user.username)
    else:
        username = Username(username=request.user.username, product_id=product_id)
        username.save()
    
    # Check if product is present in watchlist or not
    listing_check = Watchlist.objects.filter(username=username, product=product)

    # Get highest bid
    highest_bid = product.initial_bid
    bids = Bid.objects.filter(product_id=product_id)
    for bid in bids:
        if bid.bid > highest_bid:
            highest_bid = bid.bid

    # Check if product has already been closed by seller
    transaction = Transaction.objects.filter(highest_bid=highest_bid,product=product)
    if not transaction:
        closed = False
    else:
        closed = True
        transaction = Transaction.objects.get(highest_bid=highest_bid,product=product)

    if request.method == "POST":
        bid = Bid(bid=product.initial_bid,product_id=product_id)

        # Check if a bid exists in bid table, if not save the initial bid
        if not bid:
            print("checking product...")
            bid.save() # Initial bid saved

        # Check if value provided by user is higher than the highest bid
        if "value" in request.POST:
            user_bid = int(request.POST["value"])
            if user_bid > highest_bid:
                highest_bid = user_bid
            else:
                return HttpResponse("Bid must be higher than highest bid!")

        if "close" in request.POST and not transaction:
            transaction = Transaction(highest_bid=highest_bid,username=username,product=product)
            transaction.save()
            closed = True
        
        if "comment" in request.POST:
            comment = Comment(comment=request.POST["comment"], username=username)
            comment.save()
        
        # TODO: Categories
        
        
    return render(request, "auctions/product.html", {
        "product": product,
        "highest_bid": highest_bid,
        "listing_check": listing_check,
        "seller": seller,
        "closed": closed,
        "transaction": transaction,
        "comments": Comment.objects.all(),
        "categories": Category.objects.all(),
    })

def watch(request, product_id):
    if request.method == "POST":
        # Get objects for watchlist
        product = Product.objects.get(pk=product_id)
        username = Username.objects.get(username=request.user.username)

        # Make object for watchlist
        listing = Watchlist(username=username, product=product)

        # Check if listing is already on watchlist
        listing_check = Watchlist.objects.filter(username=username, product=product)
        
        if listing_check:
            if "add" in request.POST:
                listing.save()
            else:
                listing_check.delete()
        else:
            if "add" in request.POST:
                listing.save()

        return HttpResponseRedirect(reverse("auctions:product", args=(product_id,)))

def watchlist(request):
    username = Username.objects.get(username=request.user.username)
    
    watchlist = Watchlist.objects.filter(username=username)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
    })

def categories(request):
    
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    

    return render(request, "auctions/category.html", {
        "category": category,
        "products": products,
    })


