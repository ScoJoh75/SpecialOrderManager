from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
        # Captures newly saved objects information for emails.
        order_data = {'order_pk': self.object.pk,
                      'order_number': self.object.order_number,
                      'customer': self.object.customer,
                      'product_name': self.object.product_name,
                      'design_code': self.object.design_code,
                      'order_reason': self.object.order_reason,
                      'process_date': self.object.process_date,
                      'ship_date': self.object.ship_date,
                      'sequence_numbers': self.object.sequence_numbers,
                      'tooling_status': self.object.tooling_status,
                      'programming_status': self.object.programming_status,
                      'order_notes': self.object.order_notes,
                      'engineering_framing_setup': self.object.engineering_framing_setup}
        send_order_emails(order_data)
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


def send_order_emails(order_data):
    email_subject = f"Special Order: {order_data['order_number']} is ready for release"
    html_message_bvs = render_to_string('bvs_email_template.html', order_data)
    html_message_bvt = render_to_string('bvt_email_template.html', order_data)
    plain_message_bvs = strip_tags(html_message_bvs)
    plain_message_bvt = strip_tags(html_message_bvt)
    from_email = 'adiehl@conestogawood.com'
    to_bvs = []
    to_bvt = []
    contacts = Contact.objects.filter(active=True)
    for contact in contacts:
        if contact.site == 'BVS':
            to_bvs.append(contact.email_address)
        else:
            to_bvt.append(contact.email_address)

    send_mail(email_subject, plain_message_bvt, from_email, to_bvt, html_message=html_message_bvt)
    send_mail(email_subject, plain_message_bvs, from_email, to_bvs, html_message=html_message_bvs)
