from django.contrib import admin
from .models import Item, Order, OrderItem

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
