from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Order

# Create your views here.

@login_required
def index(request):
    orders = Order.objects.filter(status__name='Ready')
    return render(request, 'orders/index.html', {'orders': orders})