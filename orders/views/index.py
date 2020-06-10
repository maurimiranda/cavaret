from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from orders.models import Order, Item

@login_required
def index(request):
    pending_items = Item.objects.filter(order__status='1')\
        .values('product__provider__id', 'product__provider__name', 'product__brand__name', 'product__name')\
        .annotate(quantity=Sum('quantity'))\
        .annotate(cost=Sum('cost'))

    providers = {}

    for item in pending_items:
        provider = item['product__provider__name']
        if provider not in providers:
            providers[provider] = {
                'id': item['product__provider__id'],
                'total': 0,
                'items': []
            }

        provider = providers[provider]
        provider['total'] += item['cost']
        provider['items'].append(item)

    return render(request, 'orders/index.html', {
        'pending_items': providers,
        'ready_orders': Order.objects.filter(status__name='Ready')
    })