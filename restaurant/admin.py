from django.contrib import admin
from .models import Exclusive,Choose,Special_categories,Special_Festivals,Family_Packages
from .models import BreakFast,Veg,Non_Veg,Soups,Pasta,Snacks,Starters,CartItem
from .models import Family_Packages,Chef,Refreshing_Drinks,Quick_Bites,Combo_Offers

# Register your models here.

admin.site.register(Exclusive)
admin.site.register(Choose)
admin.site.register(Special_categories)
admin.site.register(Special_Festivals)
admin.site.register(Family_Packages)
admin.site.register(Chef)
admin.site.register(Refreshing_Drinks)
admin.site.register(Quick_Bites)
admin.site.register(Combo_Offers)
admin.site.register(BreakFast)
admin.site.register(Veg)
admin.site.register(Non_Veg)
admin.site.register(Soups)
admin.site.register(Pasta)
admin.site.register(Snacks)
admin.site.register(Starters)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "quantity", "price")
admin.site.register(CartItem, CartItemAdmin)