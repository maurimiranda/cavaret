from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('provider/<int:provider_id>/', views.provider.detail, name='provider_detail')
]