from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce

from orders.models import Order, Item, Provider


@login_required
def index(request):
    pending_items = (
        Item.objects.filter(order__status="1")
        .values(
            "product__provider__id",
            "product__provider__name",
            "product__brand__name",
            "product__name",
        )
        .annotate(quantity=Sum("quantity"))
        .annotate(cost=Sum("cost"))
    )

    providers = {}

    for item in pending_items:
        provider = item["product__provider__name"]
        if provider not in providers:
            providers[provider] = {
                "id": item["product__provider__id"],
                "total": 0,
                "quantity": 0,
                "items": [],
            }

        provider = providers[provider]
        provider["total"] += item["cost"]
        provider["quantity"] += item["quantity"]
        provider["items"].append(item)

    return render(
        request,
        "orders/index.html",
        {
            "pending_items": providers,
            "providers": Provider.objects.all,
            "pending_orders": Order.objects.filter(status__name="Pending").order_by(
                "tracking_code", "pickup_code"
            ),
            "ready_orders": Order.objects.filter(status__name="Ready").order_by(
                "tracking_code", "pickup_code"
            ),
            "sent_orders": Order.objects.filter(status__name="Sent").order_by(
                "tracking_code", "pickup_code"
            ),
        },
    )
