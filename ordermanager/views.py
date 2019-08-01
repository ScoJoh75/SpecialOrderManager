from django.shortcuts import render
from ordermanager.models import Order, Contact
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from ordermanager.forms import OrderForm
# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter().order_by('-date')


class OrderDetailView(DetailView):
    model = Order


class CreateOrderView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/order_detail.html'
    form_class = OrderForm
    model = Order


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/order_detail.html'
    form_class = OrderForm
    model = Order
