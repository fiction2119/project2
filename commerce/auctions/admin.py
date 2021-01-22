from django.contrib import admin

from .models import  Bid, Comment, Product, Username

admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Username)

