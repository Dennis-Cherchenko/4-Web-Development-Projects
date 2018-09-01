from django.contrib import admin

from .models import Pizza, Pizza_Topping, Sub, Sub_Kind_Enum, Sub_Topping, \
Pasta, Salad, Dinner_Platter, Dinner_Platter_Kind_Enum, Order, Cart_Item, Cart_Item_Pizza_Topping, Cart_Item_Sub_Topping

# Register models

admin.site.register(Pizza)
admin.site.register(Pizza_Topping)
admin.site.register(Sub)
admin.site.register(Sub_Kind_Enum)
admin.site.register(Sub_Topping)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_Platter)
admin.site.register(Dinner_Platter_Kind_Enum)
admin.site.register(Order)
admin.site.register(Cart_Item)
admin.site.register(Cart_Item_Pizza_Topping)
admin.site.register(Cart_Item_Sub_Topping)