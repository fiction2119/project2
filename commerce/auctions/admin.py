from django.contrib import admin

from .models import Listing, Bid, Comment, Product, Username

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bid", "description", "url")

class UsernameAdmin(admin.ModelAdmin):
    filter_horizontal = ("product", )

admin.site.register(Product)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Username, UsernameAdmin)

