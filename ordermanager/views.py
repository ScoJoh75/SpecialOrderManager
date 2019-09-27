from django.core.mail import send_mail
from django.shortcuts import render
from ordermanager.models import Order, Contact
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from ordermanager.forms import OrderForm, ContactForm
from datetime import datetime


# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter().order_by('-date')


class OrderDetailView(DetailView):
    model = Order


class OrderHandlingTag(DetailView):
    model = Order
    template_name = 'handling_tag.html'


class CreateOrderView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/order_detail.html'
    form_class = OrderForm
    model = Order

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.date = datetime.now()
        self.object.save()
        email_subject = f"Special Order: {self.object.order_number} is ready for release"
        send_mail(email_subject, f"Hello, this is a test for order#{self.object.order_number}",
                  "sjohnson@conestogawood.com", ["sjohnson@conestogawood.com"])
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/order_detail.html'
    form_class = OrderForm
    model = Order


class ContactListView(ListView):
    model = Contact

    def get_queryset(self):
        return Contact.objects.filter().order_by('last_name')


class ContactDetailView(DetailView):
    model = Contact


class AddContactView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/contact_detail.html'
    form_class = ContactForm
    model = Contact


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/contact_detail.html'
    form_class = ContactForm
    model = Contact
