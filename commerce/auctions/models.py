from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    url = models.CharField(max_length=200)
    initial_bid = models.IntegerField()

    def __str__(self):
        return f" Product: {self.title} | {self.description} | {self.url} | {self.initial_bid} "

class Bid(models.Model):
    bid = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.bid} | {self.product}"

class Username(models.Model):
    username = models.CharField(max_length=56)
    bids = models.ManyToManyField(Bid, blank=True, related_name="users")

    def __str__(self):
        return f"{self.username}"

class Comment(models.Model):
    commentary = models.ManyToManyField(Product, blank=True, related_name="comments")