from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=56)

    def __str__(self):
        return f"{self.category}"

class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    url = models.ImageField(upload_to="products", blank=True)
    initial_bid = models.IntegerField()
    seller = models.CharField(max_length=56)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return f" {self.title}: {self.description}"

class Bid(models.Model):
    bid = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="listing")

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

class Transaction(models.Model):
    highest_bid = models.IntegerField()
    username = models.ForeignKey(Username, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Winner: {self.username} Price: {self.highest_bid} {self.product}"
    
class Comment(models.Model):
    comment = models.CharField(max_length=250)
    username = models.ForeignKey(Username, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}: {self.comment}"
