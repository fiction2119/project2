from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    url = models.CharField(max_length=200)
    initial_bid = models.IntegerField()
    seller = models.CharField(max_length=56)
    highest_bidder = models.CharField(max_length=56, blank=True)

    def __str__(self):
        return f" {self.title}: {self.description}"

class Bid(models.Model):
    bid = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.bid} | {self.product}"

class Username(models.Model):
    username = models.CharField(max_length=56)
    bids = models.ManyToManyField(Bid, blank=True, related_name="users")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.username}"

class Watchlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="list" )
    username = models.ForeignKey(Username, on_delete=models.CASCADE, related_name="watch")
    
    def __str__(self):
        return f"{self.product}"
        
class Comment(models.Model):
    commentary = models.ManyToManyField(Product, blank=True, related_name="comments")