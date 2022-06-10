from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("providers/<int:provider_id>/", views.provider.detail, name="provider_detail"),
    path(
        "orders/<int:order_id>/update_status/<int:status_id>/",
        views.order.update_status,
        name="update_order_status",
    ),
    path("orders/<int:order_id>/pay/", views.order.pay, name="pay_order"),
    path(
        "orders/<int:order_id>/update_tracking/",
        views.order.update_tracking,
        name="update_order_tracking",
    ),
]
