from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from orders.models import Provider, Order


@login_required
def update_status(request, order_id, status_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status_id = status_id
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def pay(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.paid = True
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
