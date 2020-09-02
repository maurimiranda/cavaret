from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from orders.models import Provider


@login_required
def detail(request, provider_id):
    return render(
        request,
        "orders/provider/detail.html",
        {"provider": Provider.objects.get(pk=provider_id)},
    )
