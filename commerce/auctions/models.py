from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Product(models.Model):
    product = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.product}"

class Comment(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="heading")
    comment = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.comment}"

class Listing(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="title")
    description = models.CharField(max_length=300)
    url = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} | {self.description} | {self.url}"
    
class Username(models.Model):
    username = models.CharField(max_length=56)
    product = models.ManyToManyField(Listing, blank=True, related_name="users")

    def __str__(self):
        return f"{self.username}"

class Bid(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="name")
    initial = models.IntegerField(default=None)
    offer = models.ManyToManyField(Listing, blank=True, related_name="bid")

    def __str__(self):
        return f"{self.offer}"
