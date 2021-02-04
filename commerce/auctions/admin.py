from django.contrib import admin

from .models import  Bid, Comment, Product, Username, Watchlist, Transaction, Category

admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Username)
admin.site.register(Watchlist)
admin.site.register(Transaction)
admin.site.register(Category)

