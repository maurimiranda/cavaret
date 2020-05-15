from django.contrib import admin

# Register your models here.

from .models import (Member, Product, Provider, Brand, Status, Order, Item, Payment)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'discount')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'cost', 'price', 'profit', 'profit_percentage')

class ItemInline(admin.TabularInline):
    model = Item
    fields = ('product', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'member', 'status', 'quantity', 'total', 'paid', 'pickup_code', 'tracking_code')
    list_filter = ('status', 'paid', 'member__name')
    inlines = [ItemInline]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'price', 'cost')

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'total', 'paid', 'balance')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'amount', 'comment')

admin.site.register(Member, MemberAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Status)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Payment, PaymentAdmin)
