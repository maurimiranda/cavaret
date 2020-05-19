from django.contrib import admin

# Register your models here.

from .models import (Member, Product, Provider, Brand, Status, Order, Item, Payment)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'discount')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'cost', 'price', 'profit', 'profit_percentage')

class ItemInline(admin.TabularInline):
    model = Item
    fields = ('product', 'quantity', 'comment')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'member', 'status', 'quantity', 'total', 'paid', 'pickup_code', 'tracking_code')
    list_filter = ('status', 'paid', 'member__name')
    inlines = [ItemInline]
    actions = ['make_sent', 'make_done', 'make_ready']

    def make_ready(self, request, queryset):
        queryset.update(status=2)
    make_ready.short_description = "Mark as Ready"

    def make_sent(self, request, queryset):
        queryset.update(status=3)
    make_sent.short_description = "Mark as Sent"

    def make_done(self, request, queryset):
        queryset.update(status=4)
    make_done.short_description = "Mark as Done"

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
